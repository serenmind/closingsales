from rest_framework import serializers
from products.models import Category
from products.models import Subcategory
from products.models import Advertisement
from address.models import Country
from address.models import State
from products.models import AdImage


class CategorySerailizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'created_at')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'image', 'created_at')

class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ('id', 'subcategory', 'user', 'title', 'description', 'status',
                    'start_date', 'end_date', 'zipcode', 'address', 'address1', 'longitude', 'latitude',
                    'created_at')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name', )

class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True)
    class Meta:
        model = Country
        fields = ('id', 'name', 'currency', 'language', 'language_symbol', 'states', )


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ('id', 'file', )
