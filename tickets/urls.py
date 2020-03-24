from django.urls import path
from .views import TicketList, TicketDetail, NewTicket, ReplyTicket, GetReply, DeleteReply


urlpatterns = [
    path('api/ticket_list/', TicketList.as_view(), name='ticket_list'),
    path('api/new_ticket/', NewTicket.as_view(), name='new_ticket'),
    path('api/tickets/<int:ticket_pk>/', TicketDetail.as_view(), name='get_ticket_detail'),
    path('api/tickets/<int:ticket_pk>/reply/', ReplyTicket.as_view(), name='reply_ticket'),
    path('api/tickets/<int:ticket_pk>/replies/', GetReply.as_view(), name='get_replies'),
    path('api/replies/<int:reply_pk>/', DeleteReply.as_view(), name='delete_reply'),
]
