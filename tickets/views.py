from rest_framework.views import APIView
from utils.custom_response import CustomResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Ticket, Reply
from .serializers import TicketSerializer, ReplySerializer
from .pagination import PaginationHandlerMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


class BasicPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class TicketList(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_customer_service:
            tickets = Ticket.objects.all().order_by('-last_updated')
        else:
            tickets = Ticket.objects.filter(owner=request.user).order_by('-last_updated')
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = self.get_paginated_response(TicketSerializer(page, many=True).data)
        else:
            serializer = TicketSerializer(tickets, many=True)
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)


class TicketDetail(APIView, PaginationHandlerMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request, ticket_pk):
        ticket = Ticket.objects.get(pk=ticket_pk)
        serializer = TicketSerializer(ticket)
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)


class NewTicket(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_customer_service:
                res = {
                    "error": "You are not allowed to create a ticket. "
                }
                return CustomResponse(res, status=status.HTTP_403_FORBIDDEN)
            description = serializer.data['description']
            subject = serializer.data['subject']
            ticket = Ticket.objects.create(subject=subject, description=description, owner=user)
            # Reply.objects.create(content=content, ticket=ticket, owner=user)
            res = {
                "id": ticket.id,
                "subject": ticket.subject,
            }
            return CustomResponse(res, status=status.HTTP_201_CREATED)

        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyTicket(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            content = serializer.data['content']
            reply = Reply.objects.create(content=content, ticket=ticket, owner=user)
            ticket.last_updated = timezone.now()
            ticket.save()
            res = {
                "id": reply.id,
                "status": "Success",
            }
            return CustomResponse(res, status=status.HTTP_201_CREATED)

        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteReply(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, reply_pk):
        reply = get_object_or_404(Reply, pk=reply_pk)
        if reply.owner == request.user:
            reply.delete()
            return CustomResponse("Reply deleted", status=status.HTTP_204_NO_CONTENT)
        res = {
            "error": "You are not allowed to delete to this reply. "
        }
        return CustomResponse(res, status=status.HTTP_403_FORBIDDEN)


class GetReply(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        replies = ticket.replies.get_queryset().order_by('created_at')
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = self.get_paginated_response(ReplySerializer(page, many=True).data)
        else:
            serializer = ReplySerializer(replies, many=True)
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)
