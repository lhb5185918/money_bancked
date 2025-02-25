from rest_framework import serializers
from .models import User, Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'avatar', 'email')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'required': False},
            'email': {'required': False}
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class AccountSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Account.ACCOUNT_TYPE_CHOICES, source='account_type')
    name = serializers.CharField(source='account_name')
    
    class Meta:
        model = Account
        fields = ['account_id', 'name', 'type', 'balance', 'created_at']
        read_only_fields = ['account_id', 'created_at']

    def create(self, validated_data):
        # 将前端的type映射到模型的account_type
        account_name = validated_data.pop('account_name')
        account_type = validated_data.pop('account_type')
        balance = validated_data.get('balance', 0.00)
        
        return Account.objects.create(
            account_name=account_name,
            account_type=account_type,
            balance=balance
        ) 