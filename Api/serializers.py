from rest_framework import serializers
from .models import Booking, Transaction


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'client', 'stylist', 'date',
                  'time', 'status', 'completed', 'u_id', 'style_id']

        read_only_fields = ['client', 'stylist', 'style_id']

    def create(self, validated_data):
        client = self.context.get('client', "")
        stylist = self.context.get('stylist', "")
        style = self.context.get('style', "")

        validated_data["stylist"] = stylist
        validated_data['client'] = client
        validated_data['style_id'] = style

        return Booking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.client = validated_data.get('client', instance.client)
        instance.stylist = validated_data.get('stylist', instance.stylist)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.status = validated_data.get('status', instance.status)
        instance.completed = validated_data.get(
            'completed', instance.completed)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'booking', 'client', 'stylist',
                  'amount', 'date', 'time', 'status', 'u_id']

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.booking = validated_data.get('booking', instance.booking)
        instance.client = validated_data.get('client', instance.client)
        instance.stylist = validated_data.get('stylist', instance.stylist)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
