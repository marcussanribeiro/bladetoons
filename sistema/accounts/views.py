from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente
from .serializers import ClienteSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Usuário criado"}, status=201)

        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            cliente = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=404)

        if cliente.check_password(password):
            return Response({
                "msg": "Login OK",
                "user_id": cliente.id,
                "grupo": cliente.grupo.nome if cliente.grupo else None
            })

        return Response({"error": "Senha inválida"}, status=400)