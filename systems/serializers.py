from rest_framework.serializers import ModelSerializer
from systems import models as sys_models

class SystemParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemParameter
        fields = "__all__"


class SystemParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemParameter
        fields = "__all__"


class ListingParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.ListingParameter
        fields = "__all__"

class CurrencySerializer(ModelSerializer):
    class Meta:
        model = sys_models.Currency
        fields = "__all__"
