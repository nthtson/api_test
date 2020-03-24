from .models import Account
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=Account.objects.all())], allow_blank=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'is_customer_service', 'password')

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        account.set_password(validated_data['password'])
        account.save()
        return account
