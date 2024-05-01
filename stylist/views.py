from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Api.models import Booking, Transaction
from Api.serializers import BookingSerializer
from administration.serializers import ApprovalRequestSerializer
from authentication.models import Stylist
from authentication.serializers import StylistSerializer
from stylist.models import Style, StyleCategorie
from stylist.serializers import StyleCategorieSerializer, StyleSerializer, StyleVariationSerializer
from rest_framework.exceptions import PermissionDenied


# Create your views here.


class StylistListView(APIView):
    """Method to get all stylists"""
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            stylist = Stylist.objects.get(id=id)
            stylist_serialized = StylistSerializer(stylist).data
            return Response(stylist_serialized, status=status.HTTP_200_OK)

        except Stylist.DoesNotExist:
            return Response({"error": "Stylist not found."}, status=status.HTTP_404_NOT_FOUND)


class StylistApprovalRequestView(APIView):
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

            approval_request_serializer = ApprovalRequestSerializer(
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


class AllBookingsView(APIView):
    """Method to get bookings for a single stylist """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Implement logic for viewing all bookings per stylist
        try:
            stylist = Stylist.objects.get(user=request.user)
            stylist_bookings = Booking.objects.filter(stylist=stylist)

            serializer = BookingSerializer(stylist_bookings, many=True).data

            return Response(serializer, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingDetailView(APIView):
    """get booking details based on the u_id of the booking"""
    permission_classes = [IsAuthenticated]

    def get(self, request, u_id):

        try:
            stylist = Stylist.objects.get(user=request.user)
            booking = Booking.objects.get(u_id=u_id, stylist=stylist)
            serializer = BookingSerializer(booking).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


class BookingActionView(APIView):
    """method to reject or accept booking based on the provided action """
    permission_classes = [IsAuthenticated]

    def put(self, u_id, request, action):
        try:
            stylist = Stylist.objects.get(user=request.user)
            booking = Booking.objects.get(u_id=u_id, stylist=stylist)
            if action in dict(Booking.STATUS_CHOICES):
                booking.status = action
                booking.save()
                return Response({"msg": f"Successfully {action} the booking"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied:
            return Response({"error": f"You do not have permission to {action} this style"}, status=status.HTTP_403_FORBIDDEN)


class StylelListView(APIView):
    """method to get all styles for the single stylist"""
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            stylist = Stylist.objects.get(user=request.user)
            styles = Style.objects.filter(stylist=stylist)

            serializer = StyleSerializer(styles, many=True).data

            for style in serializer:
                style["style_category"] = StyleCategorie.objects.get(
                    id=style.get('category')).category_name
                style.pop('category')
                style.pop('stylist')

            return Response(serializer, status=status.HTTP_200_OK)

        except Stylist.DoesNotExist:
            return Response({"error": "Stylist not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """method to add a new style"""

    def post(self, request):

        try:
            stylist = Stylist.objects.get(user=request.user)

            style_data = request.data

            categorie_serializer = StyleCategorieSerializer(data=request.data)

            if categorie_serializer.is_valid():
                categorie = categorie_serializer.save()

                style_serializer = StyleSerializer(
                    data=style_data, context={'stylist': stylist, 'category': categorie})

                if style_serializer.is_valid():
                    style_serializer.save()
                    return Response({"msg": "success"}, status=status.HTTP_201_CREATED)
                return Response(style_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(categorie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StyleDetailView(APIView):
    """method to get style details"""
    permission_classes = [IsAuthenticated]

    def get(self, request, u_id):
        try:
            styles = Style.objects.get(u_id=u_id)

            serializer = StyleSerializer(styles).data
            serializer["style_category"] = StyleCategorie.objects.get(
                id=serializer.get('category')).category_name
            serializer.pop('category')
            serializer.pop('stylist')
            return Response(serializer, status=status.HTTP_200_OK)

        except Style.DoesNotExist:
            return Response({"error": "Style not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """method to update a style by the creating stylist"""

    def put(self, request, u_id):
        try:
            stylist = Stylist.objects.get(user=request.user)
            style = Style.objects.get(u_id=u_id, stylist=stylist)
            style_data = request.data

            style_serializer = StyleSerializer(data=style_data, instance=style)

            if style_serializer.is_valid():

                style_serializer.save()

                return Response({"msg": "style updated successfully"}, status=status.HTTP_200_OK)
            return Response(style_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Style.DoesNotExist:
            return Response({"error": "Style not found"}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied:
            return Response({"error": "You do not have permission to update this style"}, status=status.HTTP_403_FORBIDDEN)

    """"method to delete a style"""

    def delete(self, request, u_id):
        try:
            stylist = Stylist.objects.get(user=request.user)
            style = Style.objects.get(u_id=u_id, stylist=stylist)
            style.delete()
            return Response({"msg": "stly deleted successfullly"}, status=status.HTTP_200_OK)

        except Style.DoesNotExist:
            return Response({"error": "Style not found"}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied:
            return Response({"error": "You do not have permission to delete this style"}, status=status.HTTP_403_FORBIDDEN)


class ApproveTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, u_id):

        try:

            transaction = Transaction.objects.get(id=u_id)
            transaction.status = 'successful'
            transaction.save()
            return Response({'message': 'Transaction approved successfully'}, status=status.HTTP_200_OK)

        except transaction.DoesNotExist():
            return Response({"message": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
