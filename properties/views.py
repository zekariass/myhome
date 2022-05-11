from rest_framework import generics
from properties import serializers as prop_serializers
from properties import models as prop_models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from commons import models as cmn_models
from commons import serializers as cmn_serializers

from agents import models as agnt_models
from agents import serializers as agnt_serializers

class PropertyCategoryListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertyCategorySerializer
    permission_classes = [IsAuthenticated,]

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertyCategorySerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        # print(request.data)
        property_address = request.data.pop("address")

        property_address_serializer = cmn_serializers.AddressShortDepthSerializer(data=property_address)

        if property_address_serializer.is_valid():
            property_address_instance = property_address_serializer.save()

            if property_address_instance is not None:
                try:
                    property_category_id = request.data.pop("property_category")
                    property_category_instance = prop_models.PropertyCategory.objects.get(pk=property_category_id)
                
                except ObjectDoesNotExist:
                    print("Property category is not found!")
                    return Response(data="Property category is not found!", status=status.HTTP_404_NOT_FOUND)
                
                try:
                    agent_id = request.data.pop("agent")
                    agent_instance = agnt_models.Agent.objects.get(pk=agent_id)

                except:
                    print("Agent is not found!")
                    return Response(data="Agent is not found!", status=status.HTTP_404_NOT_FOUND)

                prop_cat_key = property_category_instance.cat_key

                apartment = condominium = traditional_house = villa = commercial_property = hall = land = None

                if prop_cat_key == "CAT001":
                    apartment = request.data.pop("apartment")
                elif prop_cat_key == "CAT002":
                    condominium = request.data.pop("condominium")
                elif prop_cat_key == "CAT003":
                    traditional_house = request.data.pop("traditional_house")
                elif prop_cat_key == "CAT004":
                    villa = request.data.pop("villa")
                elif prop_cat_key == "CAT005":
                    commercial_property = request.data.pop("commercial_property")
                elif prop_cat_key == "CAT006":
                    hall = request.data.pop("hall")
                elif prop_cat_key == "CAT007":
                    land = request.data.pop("land")
                elif prop_cat_key == "CAT008":
                    land = request.data.pop("all_purpose_property")

                property_serializer = prop_serializers.PropertyCreateBasicSerializer(data=request.data)

                if property_serializer.is_valid():
                    # print("HEYYYY! PROP IS VALID!")
                    property_instance = property_serializer.save(agent=agent_instance, address=property_address_instance, property_category=property_category_instance)
                    # print("HEYYYY! PROP IS STILL VALID!")

                    if apartment is not None:
                        # print("apartment_units: ", apartment)
                        apartment_units = apartment.pop("units")

                        apartment_serializer = prop_serializers.ApartmentCreatBasicSerializer(data=apartment)

                        if apartment_serializer.is_valid():
                            # print("HEYYYY! APARTMENT IS VALID!")
                            apartment_instance = apartment_serializer.save(property=property_instance)
                            
                            print("apartment_units: ", apartment_units)
                            apartment_unit_serializer = prop_serializers.ApartmentUnitCreateBasicSerializer(data=apartment_units, many=True)
                            print("AFTER UNIT SERIALIZER")
                            if apartment_unit_serializer.is_valid():
                                print("HEYYYY! apartment_unit_serializer IS Valid!")
                                apartment_unit_serializer.save(apartment=apartment_instance)
                            else:
                                print("Bad apartment unit data!")
                                return Response(data="Bad apartment unit data!", status=status.HTTP_400_BAD_REQUEST)
                        
                        else:
                            print("Bad apartment data!")
                            return Response(data="Bad apartment data!", status=status.HTTP_400_BAD_REQUEST)

                    elif condominium is not None:
                        pass

                else: 
                    print("Bad property data!")
                    return Response(data="Bad property data!", status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Something wrong when saving Address!")
                return Response(data="Something wrong when saving Address!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Property address not valid!")
            return Response(data="Bad address data!", status=status.HTTP_400_BAD_REQUEST)



#================================================================================

class HouseTypeListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.HouseType.objects.all()
    serializer_class = prop_serializers.HouseTypeSerializer
    permission_classes = [AllowAny,]


class BuildingTypeListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.BuildingType.objects.all()
    serializer_class = prop_serializers.HouseTypeSerializer
    permission_classes = [AllowAny,]