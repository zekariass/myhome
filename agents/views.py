from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from agents import serializers, models as agnt_models



class AgentCreateView(generics.CreateAPIView):
    serializer_class = serializers.AgentSerializer
    queryset = agnt_models.Agent.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, format=None):

        agent_data = request.data['agentData']
        agent_address = request.data['agentAddress']
        print(agent_data)

        return Response(None)