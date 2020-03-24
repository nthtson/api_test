from rest_framework import serializers
from tickets.models import Ticket, Reply
from accounts.models import Account


class TicketSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(max_length=4000, allow_blank=False)
    replies_count = serializers.SerializerMethodField(read_only=True)
    owner = serializers.CharField(read_only=True)
    ticket_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    human_time = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ticket

    def get_replies_count(self, obj):
        count = 0
        if isinstance(obj, Ticket):
            count = obj.get_replies_count()
        return count

    def get_human_time(self, obj):
        time = ''
        if isinstance(obj, Ticket):
            return obj.get_date()
        return time


class ReplySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    replied_by = serializers.CharField(source='owner.email', read_only=True)
    is_customer_service = serializers.CharField(source='owner.is_customer_service', read_only=True)
    content = serializers.CharField(max_length=4000, allow_blank=False)
    human_time = serializers.SerializerMethodField(read_only=True)

    def get_human_time(self, obj):
        time = ''
        if isinstance(obj, Reply):
            return obj.get_date()
        return time

