from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'grupo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("As senhas não coincidem")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        cliente = Cliente(**validated_data)
        cliente.set_password(password)
        cliente.save()

        return cliente