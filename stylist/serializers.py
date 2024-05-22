from .models import StyleCategorie
from .models import StyleVariation
from .models import Style
from Api.models import StylistResponse
from .models import StylistDocument
from rest_framework import serializers


class DocumentsSerializer(serializers.ModelSerializer):

    profile_picture = serializers.ImageField(required=True)
    national_id_front = serializers.ImageField(required=True)
    national_id_back = serializers.ImageField(required=True)
    good_conduct_cert = serializers.ImageField(required=True)

    class Meta:
        model = StylistDocument
        fields = ['profile_picture', 'national_id_front',
                  'national_id_back', 'good_conduct_cert', 'stylist_id',]


class BaseResponseSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)

    class Meta:
        model = StylistResponse
        fields = ['id', 'content', 'stylist_id', 'questionnaire_id']


class StyleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Style
        fields = ['id', 'name', 'description', 'stylist', 'category', 'u_id']

        """ What this does is during serialization the read
            only fields will be availble in the json
            but during deserialization their value will be determined
            Since you want the serializer to automatically set the style
            based on the newly created Style object, we mark it as read-only
            during object creation. This means that the user cannot specify
            the style directly when creating a StyleVariation object
        """
        read_only_fields = ['stylist', 'category', 'u_id']

    def create(self, validated_data):
        stylist = self.context.get('stylist')
        category = self.context.get('category')
        validated_data['stylist'] = stylist
        validated_data['category'] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.stylist = validated_data.get('stylist', instance.stylist)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class StyleVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleVariation
        fields = ['id', 'name', 'price', 'photo',
                  'video', 'style', 'u_id', 'length']
        read_only_fields = ['u_id', 'style']

    def create(self, validated_data):
        style = self.context['style']
        validated_data['style'] = style
        return StyleVariation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.video = validated_data.get('video', instance.video)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class StyleCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleCategorie
        fields = '__all__'
        read_only_fields = ['u_id']

    def create(self, validated_data):
        style = StyleCategorie.objects.create(**validated_data)
        return style

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get(
            'category_name', instance.category_name)
        instance.save()
        return instance
