from rest_framework import serializers

from administration.models import ApprovalRequest


class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ['id', 'date', 'time', 'stylist_id','status']

    def create(self, validated_data):
        approval_instance = ApprovalRequest.objects.create(**validated_data)
        return approval_instance
