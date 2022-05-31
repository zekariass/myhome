from rest_framework.serializers import ModelSerializer
from systems import models as sys_models

class SystemParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemParameter
        fields = "__all__"
