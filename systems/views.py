from django.shortcuts import render

from rest_framework import generics
from systems import serializers as sys_serializers
from systems import models as sys_models
from rest_framework.permissions import AllowAny

class SystemParameterListView(generics.ListAPIView):
    queryset = sys_models.SystemParameter.objects.all()
    serializer_class = sys_serializers.SystemParameterSerializer
    permission_classes = [AllowAny,]
