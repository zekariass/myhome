from attr import fields
from rest_framework import serializers
from properties import models as prop_models
from commons import serializers as cmn_serializers
from agents import serializers as agnt_serializers

#===========PROPERTY=======================================================================
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
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyImage
        exclude = ("property",)

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        exclude = ("property",)

class PropertyFileLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyFileLabel
        fields = "__all__"
#==========================================================================================
#===========APARTMENT======================================================================

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        fields = "__all__"

class ApartmentCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        exclude = ("property",)

class ApartmentUnitSerializer(serializers.ModelSerializer):
    apartment = ApartmentCreateBasicSerializer()
    class Meta:
        model = prop_models.ApartmentUnit
        fields = "__all__"

class ApartmentUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ApartmentUnit
        exclude = ("apartment",)
#==========================================================================================
#===========CONDOMINIUM====================================================================
class CondominiumCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Condominium
        exclude = ("property",)
#==========================================================================================
#===========VILLA==========================================================================
class VillaCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Villa
        exclude = ("property",)
#==========================================================================================
#===========TRADITIONAL HOUSE==============================================================
class TraditionalHouseCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TraditionalHouse
        exclude = ("property",)
#==========================================================================================
#===========SHARE HOUSE====================================================================
class ShareHouseCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ShareHouse
        exclude = ("property",)
#==========================================================================================
#===========COMMERCIAL PROPERTY============================================================
class CommercialPropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.CommercialProperty
        exclude = ("property",)

class CommercialPropertyUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.CommercialPropertyUnit
        exclude = ("commercial_property",)
#==========================================================================================
#===========LAND===========================================================================
class LandCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Land
        exclude = ("property",)
#==========================================================================================
#===========ALL PURPOSE PROPERTY===========================================================
class AllPurposePropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposeProperty
        exclude = ("property",)

class AllPurposePropertyUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposePropertyUnit
        exclude = ("all_purpose_property",)
#==========================================================================================
#===========HALL===========================================================================
class HallCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Hall
        exclude = ("property",)
#==========================================================================================
#===========OFFICE=========================================================================
class OfficeCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Office
        exclude = ("property",)
#==========================================================================================
#===========HOUSE TYPE=====================================================================
class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.HouseType
        fields = "__all__"
#==========================================================================================
#===========BUILDING TYPE==================================================================
class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.BuildingType
        fields = "__all__"
#==========================================================================================
#===========???????????====================================================================