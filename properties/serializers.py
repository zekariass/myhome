from attr import fields
from rest_framework import serializers
from properties import models as prop_models
from commons import serializers as cmn_serializers
from agents import serializers as agnt_serializers

class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"

class PropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Property
        fields = ["id","is_residential","description", "added_on"]
        extra_kwargs = {'added_on': {'read_only': True}, "id":{"read_only":True}}

class PropertySerializer(serializers.ModelSerializer):
    property_category = PropertyCategorySerializer()
    address = cmn_serializers.AddressSerializer()
    agent = agnt_serializers.AgentSerializer()
    class Meta:
        model = prop_models.Property
        fields = "__all__"

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        fields = "__all__"

class ApartmentCreatBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        exclude = ("property",)

class ApartmentUnitSerializer(serializers.ModelSerializer):
    apartment = ApartmentCreatBasicSerializer()
    class Meta:
        model = prop_models.ApartmentUnit
        fields = "__all__"

class ApartmentUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ApartmentUnit
        exclude = ("apartment",)


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.HouseType
        fields = "__all__"


class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.BuildingType
        fields = "__all__"