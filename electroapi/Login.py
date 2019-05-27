from accounts.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings


from .serializers import TokenSerializer, UserSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        phone = request.data.get("phone", "")
        password = request.data.get("password", "")

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            user = User.objects.get(phone__iexact=phone)

        if user.check_password(password):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
