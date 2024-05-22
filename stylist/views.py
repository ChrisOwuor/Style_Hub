from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Api.models import Booking, Transaction
from Api.serializers import BookingSerializer
from administration.serializers import ApprovalRequestSerializer
from authentication.models import Stylist
from authentication.serializers import StylistSerializer
from stylist.models import Style, StyleCategorie, StyleVariation, StylistDocument
from stylist.serializers import DocumentsSerializer, StyleCategorieSerializer, StyleSerializer, StyleVariationSerializer
from rest_framework.exceptions import PermissionDenied


# Create your views here.


class StylistListView(APIView):
    """Method to get all stylists"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            stylists = Stylist.objects.all()
            stylists_serialized = StylistSerializer(stylists, many=True).data
            for stylist in stylists_serialized:
                stylist_documents = StylistDocument.objects.filter(
                    stylist_id=stylist.get("id"))
                serilized_documents = DocumentsSerializer(
                    stylist_documents, many=True).data
                serilized_documents[0].pop("stylist_id")
                stylist["documents"] = serilized_documents

            return Response(stylists_serialized, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": "An error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StylistDetailView(APIView):
    """Method to get single stylist details"""
    permission_classes = [IsAuthenticated]

    def get(self, request, u_id):
        try:
            stylist = Stylist.objects.get(u_id=u_id)
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

    def put(self, request,  u_id, action):
        try:
            stylist = Stylist.objects.get(user=request.user)
            booking = Booking.objects.get(u_id=u_id, stylist=stylist)
            if action in dict(Booking.STATUS_CHOICES):
                booking.status = action
                booking.save()
                if action == "confirmed":
                    stylist.availability = False
                    stylist.save()
                return Response({"msg": f"Successfully {action} the booking"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied:
            return Response({"error": f"You do not have permission to {action} this style"}, status=status.HTTP_403_FORBIDDEN)


class StylelListView(APIView):
    permission_classes = [IsAuthenticated]

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


class VariationListView(APIView):
    """method to add a new variation"""

    def post(self, request):

        try:
            style = Style.objects.get(u_id=request.data.get("u_id"))

            variation_serializer = StyleVariationSerializer(
                data=request.data, context={"style": style})

            if variation_serializer.is_valid():
                variation_serializer.save()

                return Response({"msg": "success"}, status=status.HTTP_201_CREATED)

            return Response(variation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Style.DoesNotExist:
            return Response({"error":"style not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class CategoryView(APIView):
    """method to get all categories"""
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            categories = StyleCategorie.objects.all()
            serializer = StyleCategorieSerializer(categories, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = StyleCategorieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "success"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
