from accounts.models import User, City
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from .serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        user_category = request.data.get("user_category", "")
        phone = request.data.get("phone", "")
        city = request.data.get("city", "")
        date_of_birth = request.data.get("date_of_birth", "")

        try:
            phone_number = User.objects.get(phone__iexact=phone)
            a_email = User.objects.get(phone__iexact=phone)
            return Response(
                data={
                    "message": "phone or email has been used"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except:
            a_city = City.objects.get(name__iexact=city)
            new_user = User.objects.create_user(
                first_name=first_name, password=password, last_name=last_name, phone=phone,
                email=email, user_category=user_category, city=a_city, date_of_birth=date_of_birth
            )

            return Response(
                data=UserSerializer(new_user).data,
                status=status.HTTP_201_CREATED
            )


