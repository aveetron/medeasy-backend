from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer
from validate_email import validate_email


class RegisterAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        payload = request.data
        try:
            """ check this email is valid in network """
            is_valid_email = validate_email(payload["email"])
            if not is_valid_email:
                return Response({
                    "data": {},
                    "response_message": "Invalid email address",
                    "response_code": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

            user_serializer = UserSerializer(data=payload)
            if user_serializer.is_valid():
                """ 
                    account activation
                """
                user_serializer.save(is_active=True)
                return Response({
                    "data": {},
                    "response_message": "user created successfully & mail sent for verification.",
                    "response_code": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "data": {},
                    "response_message": user_serializer.errors,
                    "response_code ": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {},
                "response_message": e.args[0],
                "response_code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)