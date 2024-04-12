'''
Test for successful client and stylist registration.
Test for invalid data input.
Test for duplicate user registration.
MyTokenObtainPairView:

Test for successful token generation upon login.
Test for invalid credentials.
Test for unauthorized access.
RequestOTPView:

Test for successful OTP request.
Test for invalid email input.
Test for email sending failure.
VerifyOTPView:

Test for successful OTP verification.
Test for OTP verification failure (e.g., invalid OTP, expired OTP).
Test for unauthorized access (e.g., user tries to verify OTP for another user).
ResetPasswordView:

Test for successful password reset.
Test for password reset failure (e.g., invalid OTP, expired OTP, invalid user).
Test for unauthorized access.

'''


from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User, Client
from authentication.serializers import BaseUserSerializer, ClientSerializer


class ClientRegisterAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_client_registration_success(self):
        # Make a POST request to register a new client
        response = self.client.post(
            'client/register', {'email': 'client@example.com', 'user_name': 'Cliento', 'password': 'client123'})

        # Check if the response is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the new client is created in the database
        self.assertTrue(User.objects.filter(
            email='client@example.com').exists())
        self.assertTrue(User.objects.filter(role='client').exists())
        self.assertTrue(Client.objects.filter(
            user__email='client@example.com').exists())


