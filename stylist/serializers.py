from .models import Questionnaire, Document, UserResponse
from rest_framework import serializers


class DocumentsSerializer(serializers.ModelSerializer):

    profile_picture = serializers.ImageField(required=True)
    national_id_front = serializers.ImageField(required=True)
    national_id_back = serializers.ImageField(required=True)
    good_conduct_cert = serializers.ImageField(required=True)

    class Meta:
        model = Document
        fields = ['profile_picture', 'national_id_front',
                  'national_id_back', 'good_conduct_cert', 'stylist_id',]


class BaseResponseSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)

    class Meta:
        model = UserResponse
        fields = ['id', 'content', 'stylist_id', 'questionnaire_id']


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['id', 'question',]
