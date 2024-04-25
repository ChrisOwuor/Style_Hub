from rest_framework.views import APIView
from rest_framework import status
from administration.models import ApprovalRequest
from administration.serializers import AprrovalRequestSerializer
from rest_framework.response import Response

from authentication.models import Stylist

# Create your views here.


class AdminApprovalsListView(APIView):

    def get(self, request):
        approvals = ApprovalRequest.objects.all()

        approvals_serializer = AprrovalRequestSerializer(approvals, many=True)
        for approval in approvals_serializer.data:
            stylist = Stylist.objects.get(id=approval.get('stylist_id'))
            approval['name'] = stylist.user.full_name
            approval.pop('stylist_id')

        return Response(approvals_serializer.data, status=status.HTTP_200_OK)


class AdminApprovalsActionView(APIView):

    def put(self, request, id, action):
        try:
            approval_req = ApprovalRequest.objects.get(id=id)
            approval_req.status = action
            approval_req.stylist_id.verified = True
            approval_req.stylist_id.save()
            print(approval_req.stylist_id.verified)
            approval_req.save()
            return Response(approval_req.status)
        except ApprovalRequest.DoesNotExist():
            return Response({"error": "Approval Request not found"})
