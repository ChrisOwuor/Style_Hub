# views.py
import json
from authentication.models import Otp, User
from style_hub import settings
from stylist.models import Questionnaire
from stylist.serializers import BaseResponseSerializer, DocumentsSerializer
from .serializers import OtpVerifySerializer, ResetPasswordSerializer, StylistSerializer, OtpSerializer, ClientSerializer, AdminSerializer, BaseUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
from django.conf import settings
from django.utils.html import strip_tags
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser


class AdminRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role == "admin":
            user_serializer = BaseUserSerializer(data=request.data)

            if user_serializer.is_valid():
                new_user = user_serializer.save()

                admin_data = {
                    'user': new_user.id,
                }
                admin_serializer = AdminSerializer(data=admin_data)

                if admin_serializer.is_valid():
                    admin_serializer.save()

                    return Response(user_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    new_user.delete()
                    return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Unauthorized you cant create an admi  user"}, status=status.HTTP_401_UNAUTHORIZED)


class ClientRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, ):
        request.data['role'] = 'client'
        user_serializer = BaseUserSerializer(data=request.data)
        if user_serializer.is_valid():
            new_client = user_serializer.save()
            client_data = {
                'user': new_client.id,
            }
            client_serializer = ClientSerializer(data=client_data)
            if client_serializer.is_valid():
                client_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            else:
                new_client.delete()
                return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StylistRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            request.data['role'] = 'stylist'

            user_serializer = BaseUserSerializer(data=request.data)
            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            new_stylist = user_serializer.save()

            stylist_data = {
                "user":  new_stylist.id,
                "user_name": request.data.get('user_name', ""),
                "date_of_birth": request.data.get('date_of_birth', None),
                "phone_number": request.data.get('phone_number', ""),
                "residency": request.data.get('residency', ""),
                "next_of_kin_name": request.data.get('next_of_kin_name', ""),
                "next_of_kin_phone": request.data.get('next_of_kin_phone', ""),
                "emergency_contact_name": request.data.get('emergency_contact_name', ""),
                "emergency_contact_phone": request.data.get('emergency_contact_phone', ""),
                "gender": request.data.get('gender', "Female"),
                "location": request.data.get('location', "")
            }

            stylist_serializer = StylistSerializer(data=stylist_data)
            if not stylist_serializer.is_valid():
                new_stylist.delete()
                return Response(stylist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            created_stylist = stylist_serializer.save()

            document_fields = {
                "profile_picture": request.data.get('profile_picture', None),
                "national_id_front": request.data.get('national_id_front', None),
                "national_id_back": request.data.get('national_id_back', None),
                "good_conduct_cert": request.data.get('good_conduct_cert', None),
                "stylist_id": created_stylist.id
            }

            document_serializer = DocumentsSerializer(data=document_fields)
            if not document_serializer.is_valid():
                new_stylist.delete()
                created_stylist.delete()
                return Response(document_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            created_document = document_serializer.save()

            client_res_str = request.data.get('client_res', '[]')
            client_res = json.loads(client_res_str)
            if not client_res:
                new_stylist.delete()
                created_stylist.delete()
                created_document.delete()
                return Response({"msg": "Client responses required"}, status=status.HTTP_400_BAD_REQUEST)

            for item in client_res:
                question_id = item['id']
                content = item['content']

                questionnaire = Questionnaire.objects.get(id=question_id)

                response_data = {
                    'content': content,
                    'questionnaire_id': questionnaire.id,
                    'stylist_id': created_stylist.id,
                }

                serializer = BaseResponseSerializer(data=response_data)
                if not serializer.is_valid():
                    new_stylist.delete()
                    created_stylist.delete()
                    created_document.delete()
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            if new_stylist:
                new_stylist.delete()
            if created_stylist:
                created_stylist.delete()
            if created_document:
                created_document.delete()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["role"] = user.role
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Password Recovery


class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get("email", "")
        if not email:
            return Response({"msg": "No email entered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "No user found with the provided credentials"}, status=status.HTTP_404_NOT_FOUND)

        otp = Otp.objects.create(
            created_for=user,
            code=Otp.get_code()
        )
        otp_serializer = OtpSerializer(otp).data

        html_template_path = os.path.join(
            settings.BASE_DIR, "authentication", "templates", "mailtemp.html")
        subject = "Email Verification"
        message = ""
        sender = f"(Nuymba Nywele) <{settings.EMAIL_HOST_USER}>"
        recepient = [user.email]
        context = {
            "user": user,
            "otp": otp_serializer["code"]
        }

        html_message = render_to_string(
            html_template_path, context)
        plain_message = strip_tags(html_message)

        try:
            message = EmailMultiAlternatives(
                subject,
                plain_message,
                sender,
                [recepient],
            )
            message.attach_alternative(html_message, "text/html")
            message.send()
            return Response({'msg': 'OTP successfully sent to mail.', 'code': user.u_id}, status=status.HTTP_200_OK)
        except Exception as e:
            otp.delete()
            return Response({'msg': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OtpVerifySerializer(data=request.data)
        if serializer.is_valid():
            u_id = serializer.validated_data['u_id']
            otp = serializer.validated_data['otp']

            try:
                user = User.objects.get(u_id=u_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid user"}, status=status.HTTP_404_NOT_FOUND)

            try:
                otp_instance = Otp.objects.get(created_for=user.id, code=otp)
            except Otp.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            if otp_instance.is_verified:
                return Response({'error': 'OTP already verified, proceed to reset password'}, status=status.HTTP_400_BAD_REQUEST)

            if not otp_instance.is_valid():
                otp_instance.delete()
                return Response({'error': 'OTP has expired, request another one'}, status=status.HTTP_400_BAD_REQUEST)

            otp_instance.is_verified = True
            otp_instance.save()
            return Response({'success': 'OTP verified successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password1']
            u_id = serializer.validated_data['u_id']

            try:
                user = User.objects.get(u_id=u_id)
            except User.DoesNotExist:
                return Response({"error": "No user found with the provided credentials"}, status=status.HTTP_404_NOT_FOUND)

            try:
                otp_instance = Otp.objects.filter(
                    created_for=user.id, is_verified=True)
            except Otp.DoesNotExist:
                return Response({"error": "request OTP and verify before you proceed to reset password"}, status=status.HTTP_404_NOT_FOUND)
            if otp_instance.exists():

                user.set_password(password)
                user.save()
                otp_instance.delete()
                return Response({'success': 'Password reset successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
