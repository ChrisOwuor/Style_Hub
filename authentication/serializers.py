from rest_framework import serializers

from Api.models import Otp
from .models import User, Admin, Client, Stylist


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
        from rest_framework import serializers


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)
    u_id = serializers.UUIDField()

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError(
                {"password_match_error": "Passwords do not match"})

        return data


class OtpVerifySerializer(serializers.Serializer):
    u_id = serializers.UUIDField()
    otp = serializers.CharField(max_length=4, min_length=4)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                {"otp_error": "OTP must contain  digits."})
        return value


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = self.context.get("role", "")
        validated_data['role'] = role

        password = validated_data.pop('password', None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            # we hash the password
            instance.set_password(password)

        instance.save()
        # we can now return our stored user
        return instance

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.user_name = validated_data.get(
            'user_name', instance.user_name)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.role = validated_data.get('role', instance.role)
        instance.u_id = validated_data.get('u_id', instance.u_id)
        instance.save()
        return instance


class AdminSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Admin
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin

    def update(self, instance, validated_data):
        instance.user.email = validated_data.get(
            'user', {}).get('email', instance.user.email)
        instance.user.user_name = validated_data.get(
            'user', {}).get('user_name', instance.user.user_name)
        instance.user.start_date = validated_data.get(

            'user', {}).get('start_date', instance.user.start_date)
        instance.user.is_staff = validated_data.get(
            'user', {}).get('is_staff', instance.user.is_staff)
        instance.user.is_active = validated_data.get(
            'user', {}).get('is_active', instance.user.is_active)
        instance.user.role = validated_data.get(
            'user', {}).get('role', instance.user.role)
        instance.user.u_id = validated_data.get(
            'user', {}).get('u_id', instance.user.u_id)
        instance.user.save()
        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        return client

    def update(self, instance, validated_data):
        instance.user.email = validated_data.get(
            'user', {}).get('email', instance.user.email)
        instance.user.user_name = validated_data.get(
            'user', {}).get('user_name', instance.user.user_name)
        instance.user.start_date = validated_data.get(
            'user', {}).get('start_date', instance.user.start_date)
        instance.user.is_staff = validated_data.get(
            'user', {}).get('is_staff', instance.user.is_staff)
        instance.user.is_active = validated_data.get(
            'user', {}).get('is_active', instance.user.is_active)
        instance.user.role = validated_data.get(
            'user', {}).get('role', instance.user.role)
        instance.user.u_id = validated_data.get(
            'user', {}).get('u_id', instance.user.u_id)
        instance.user.save()
        instance.save()
        return instance


class StylistSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    phone_number = serializers.CharField(required=True)
    residency = serializers.CharField(required=True)
    next_of_kin_name = serializers.CharField(required=True)
    next_of_kin_phone = serializers.CharField(required=True)
    emergency_contact_name = serializers.CharField(required=True)
    emergency_contact_phone = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    location = serializers.CharField(required=True)

    class Meta:
        model = Stylist
        fields = '__all__'

    def create(self, validated_data):
        stylist = Stylist.objects.create(**validated_data)
        return stylist

    def update(self, instance, validated_data):
        pass
