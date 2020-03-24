from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from utils.custom_response import CustomResponse
from .serializers import AccountSerializer


class AccountCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)


class AccountDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)
