from rest_framework.decorators import action
from rest_framework import viewsets,status
from rest_framework.response import Response
from api.models import CustomUserModel
from api.serializers import CustomUserModelSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class AuthenticationViewSet(viewsets.ModelViewSet):
    serializer_class=CustomUserModelSerializer
    permission_classes=[AllowAny]
    queryset=CustomUserModel.objects.all()

    @action(detail=False,methods=['POST'],url_path='signup')
    def sign_up(self,request):
        data=request.data
        serializer=CustomUserModelSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                "success":False,
                "message":"Signup failed",
                "errors":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "success":True,
            "message":"SignUp Successfull",
            "data":serializer.data
        },status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            return Response({"success": False, "message": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"success": False, "message": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
