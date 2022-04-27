from rest_framework.serializers import ModelSerializer
from agents import models as agnt_models

class AgentLogoSerializer(ModelSerializer):
    class Meta:
        model = agnt_models.AgentLogo
        fields = "__all__"


class AgentSerializer(ModelSerializer):
    class Meta:
        model = agnt_models.Agent
        fields = "__all__"