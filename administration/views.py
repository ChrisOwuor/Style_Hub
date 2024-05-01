from rest_framework.views import APIView
from rest_framework import status
from administration.models import ApprovalRequest
from administration.serializers import ApprovalRequestSerializer
from rest_framework.response import Response

from authentication.models import Stylist

# Create your views here.


class AdminApprovalsListView(APIView):

    def get(self, request):
        try:
            approvals = ApprovalRequest.objects.all()

            serializer = ApprovalRequestSerializer(approvals, many=True)
            for approval in serializer.data:
                stylist_id = approval.get('stylist_id')

                if stylist_id:
                    stylist = Stylist.objects.get(id=stylist_id)
                    approval['name'] = stylist.user.full_name

                approval.pop('stylist_id', None)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):

        try:

            approvals = ApprovalRequest.objects.all()
            approvals.delete()
            return Response({"message": "Objects deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(f"error {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminApprovalsActionView(APIView):
    def put(self, request, id, action):
        try:
            approval_req = ApprovalRequest.objects.get(id=id)
            approval_req.status = action
            approval_req.save()

            stylist = approval_req.stylist_id
            stylist.verified = True
            stylist.save()

            return Response({"message": "Approval request updated successfully."}, status=status.HTTP_200_OK)
        except ApprovalRequest.DoesNotExist:
            return Response({"error": "Approval request not found."}, status=status.HTTP_404_NOT_FOUND)
