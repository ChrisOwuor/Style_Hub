from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from administration.serializers import AprrovalRequestSerializer
from authentication.models import Stylist
from authentication.serializers import StylistSerializer

# Create your views here.


class StylistListView(APIView):
    """Method to get all stylists"""

    def get(self, request):
        try:
            stylists = Stylist.objects.all()
            stylists_serialized = StylistSerializer(stylists, many=True).data
            return Response(stylists_serialized, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": "An error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StylistDetailView(APIView):
    """Method to get single stylist details"""

    def get(self, request, id):
        try:
            stylist = Stylist.objects.get(id=id)
            stylist_serialized = StylistSerializer(stylist).data
            return Response(stylist_serialized, status=status.HTTP_200_OK)

        except Stylist.DoesNotExist:
            return Response({"error": "Stylist not found."}, status=status.HTTP_404_NOT_FOUND)


class StylistApprovalView(APIView):
    """Method to create an approval request by stylist"""

    def post(self, request):
        try:
            stylist_id = request.data.get("stylist_id")
            date_str = request.data.get("date")
            time_str = request.data.get("time")

            if not (stylist_id and date_str and time_str):
                return Response({"error": "Stylist ID, date, and time are required for approval bookings."},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                stylist = Stylist.objects.get(id=stylist_id)
            except Stylist.DoesNotExist:
                return Response({"error": "Stylist not found."}, status=status.HTTP_404_NOT_FOUND)

            approval_data = {
                "date": date_str,
                "time": time_str,
                "stylist_id": stylist.id
            }

            approval_request_serializer = AprrovalRequestSerializer(
                data=approval_data)
            if approval_request_serializer.is_valid():
                approval_request_serializer.save()
                new_approval = approval_request_serializer.data
                new_approval['name'] = stylist.user.full_name
                return Response(new_approval, status=status.HTTP_201_CREATED)
            else:
                return Response(approval_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": "An error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
