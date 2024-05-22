from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from Api.models import Booking
from Api.serializers import BookingSerializer
from authentication.models import Client, Stylist
from authentication.serializers import ClientSerializer
from stylist.models import Style, StyleCategorie, StyleVariation
from stylist.serializers import StyleSerializer, StyleVariationSerializer


class ClientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            clients = Client.objects.all()
            serializer = ClientSerializer(clients, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, u_id):
        try:
            client = Client.objects.get(u_id=u_id)
            client_serialized = ClientSerializer(client).data
            client_serialized.pop('user')
            return Response(client_serialized, status=status.HTTP_200_OK)

        except Client.DoesNotExist:
            return Response({"error": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StyleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            styles = Style.objects.all()

            serializer = StyleSerializer(styles, many=True).data

            for style in serializer:
                variations = StyleVariation.objects.filter(style=style["id"])
                serialized_variations = StyleVariationSerializer(
                    variations, many=True).data
                style["style_category"] = StyleCategorie.objects.get(
                    id=style.get('category')).category_name
                style['stylist'] = Stylist.objects.get(
                    id=style['stylist']).user_name
                style['variations'] = serialized_variations
                style.pop('category')

            return Response(serializer, status=status.HTTP_200_OK)

        except Style.DoesNotExist:
            return Response({"error": "Stylist not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        pass


class StyleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, u_id):
        try:
            styles = Style.objects.get(u_id=u_id)

            serializer = StyleSerializer(styles).data
            serializer["style_category"] = StyleCategorie.objects.get(
                id=serializer.get('category')).category_name
            serializer['stylist'] = Stylist.objects.get(
                id=serializer['stylist']).user_name

            serializer.pop('category')
            return Response(serializer, status=status.HTTP_200_OK)

        except Style.DoesNotExist:
            return Response({"error": "Style not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, u_id):
        ...

    def delete(self, request, u_id):
        ...


class StyleCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category):

        try:
            category = StyleCategorie.objects.get(name=category)
            styles = Style.objects.filter(category=category)
            serializer = StyleSerializer(styles, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)

        except StyleCategorie.DoesNotExist:
            return Response({"msg": "category missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            client = Client.objects.get(user=request.user)
            bookings = Booking.objects.filter(client=client.id)

            serializer = BookingSerializer(bookings, many=True).data

            for booking in serializer:
                styles = Style.objects.get(id=booking["style_id"])
                serialized_styles = StyleSerializer(
                    styles).data
                booking["stylist_name"] = Stylist.objects.get(
                    id=booking["stylist"]).user_name
                booking["style"] = serialized_styles
                booking.pop('client')
                booking.pop('style_id')
                booking.pop('stylist')

            return Response(serializer, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            u_id = request.data.get("u_id")
            client = Client.objects.get(user=request.user)
            style = Style.objects.get(u_id=u_id)
            if not style.stylist.availability:
                return Response({"error": "stylist not available for bookig right now"}, status=status.HTTP_200_OK)

            booking_serializer = BookingSerializer(data=request.data, context={
                "style": style, "client": client, "stylist": style.stylist})

            if booking_serializer.is_valid():
                booking_serializer.save()
                return Response({"message": "successfully booked"}, status=status.HTTP_200_OK)
            return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response({"msg": "client missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Stylist.DoesNotExist:
            return Response({"msg": "stylist missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, u_id):
        ...

    def delete(self, request, u_id):
        ...
