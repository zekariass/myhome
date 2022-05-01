from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ObjectDoesNotExist

from agents import serializers, models as agnt_models
from commons import models as cmn_models
from commons import serializers as cmn_serializers



class AgentCreateView(generics.CreateAPIView):
    """
    Agent create view
    """
    serializer_class = serializers.AgentSerializer
    queryset = agnt_models.Agent.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, format=None):
        # Extract agent and agent address data from request
        agent_with_request_user = None
        try:
            # Check if the request user has attached agent already
            agent_with_request_user = agnt_models.AgentAdmin.objects.get(admin=request.user)
        except agnt_models.AgentAdmin.DoesNotExist:

            if agent_with_request_user is None:
                agent_address = request.data['agentAddress']
                agent_data = request.data['agentData']

                # Get agent and address objects from DB
                country = cmn_models.Country.objects.get(pk=agent_address['country'])
                region = cmn_models.Region.objects.get(pk=agent_address['region'])
                city = cmn_models.City.objects.get(pk=agent_address['city'])
                
                #Deserialize Address data
                address_serializer = cmn_serializers.AddressSerializer(data=agent_address)
                #Deserialize Agent data
                agent_serializer = self.get_serializer(data=agent_data)

                if address_serializer.is_valid() and agent_serializer.is_valid():
                    # Create address instance of the agent
                    address_instance = address_serializer.save(country=country, region=region, city=city)
                    
                    # Create the agent instance
                    agent_instance = agent_serializer.save(address=address_instance)

                    # Create the AgentAdmin intance and set the current user as manager of the agent
                    agnt_models.AgentAdmin.objects.create(agent=agent_instance, admin=request.user, is_manager=True)
                    return Response(agent_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data="Bad request data found!", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data="You have an existing agent with this user!", status=status.HTTP_409_CONFLICT)
        else:
            return Response(data="You have an existing agent with this user!", status=status.HTTP_409_CONFLICT)

#========================================================================================================

class AgentRetrieveView(APIView):
    """
    Get specific Agent with full data (including Address and Logo )
    """
    # queryset = agnt_models.Agent.objects.all()
    # serializer_class = serializers.AgentFullDataSerializer
    # permission_classes = [IsAuthenticated]
    # lookup_field = []

    def get(self, request, **kwargs):
        user = request.user
        try:
            agent = agnt_models.Agent.objects.get(manager=user)
            serialized_data = serializers.AgentFullDataSerializer(agent, context={"request": request})
            return Response(data=serialized_data.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            try:
                agent_admin = agnt_models.AgentAdmin.objects.get(admin=user)
                agent = agnt_models.Agent.objects.get(pk=agent_admin.agent.pk)
                serialized_data = serializers.AgentFullDataSerializer(agent, context={"request": request})
                return Response(data=serialized_data.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(data="No Agent found!", status=status.HTTP_404_NOT_FOUND)
            


#========================================================================================================

class AgentLogoCreateView(generics.CreateAPIView):
    """
    Upload a logo for a specific agent
    """
    queryset = agnt_models.AgentLogo.objects.all()
    serializer_class = serializers.AgentLogoSerializer
    parser_clasess = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        data = request.data
        agent_id = data.pop("agent")
        logo_serializer = self.get_serializer(data=data)
        if logo_serializer.is_valid():
            logo_instance = logo_serializer.save()
            
            agnt_models.Agent.objects.filter(pk=agent_id[0]).update(logo=logo_instance)
            return Response(data = logo_serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(data="Bad request data", status=status.HTTP_400_BAD_REQUEST)


class AgentLogoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AgentLogoSerializer
    queryset = agnt_models.AgentLogo.objects.all()
