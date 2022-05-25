from rest_framework import generics
from properties import serializers as prop_serializers
from properties import models as prop_models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser, FormParser

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
        print(request.data)
        property_address = request.data.pop("address")
        unresolved_sub_property_data = request.data.pop("category")

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

                except ObjectDoesNotExist:
                    print("Agent is not found!")
                    return Response(data="Agent is not found!", status=status.HTTP_404_NOT_FOUND)

                prop_cat_key = property_category_instance.cat_key

                # apartment = condominium = traditional_house = villa = commercial_property = hall = office = \
                # land = share_house = all_purpose_property = None

                units = units_serializer = resolved_sub_property_serializer = None


                if prop_cat_key == "CAT001":
                    apartment = unresolved_sub_property_data.pop("apartment")
                    units = apartment.pop("units")
                    resolved_sub_property_serializer = prop_serializers.ApartmentCreateBasicSerializer(data=apartment)
                    units_serializer = prop_serializers.ApartmentUnitCreateBasicSerializer(data=units, many=True)
                elif prop_cat_key == "CAT002":
                    condominium = unresolved_sub_property_data.pop("condominium")
                    resolved_sub_property_serializer = prop_serializers.CondominiumCreateBasicSerializer(data=condominium)
                elif prop_cat_key == "CAT003":
                    traditional_house = unresolved_sub_property_data.pop("traditional_house")
                    resolved_sub_property_serializer = prop_serializers.TraditionalHouseCreateBasicSerializer(data=traditional_house)
                elif prop_cat_key == "CAT004":
                    villa = unresolved_sub_property_data.pop("villa")
                    resolved_sub_property_serializer = prop_serializers.VillaCreateBasicSerializer(data=villa)
                elif prop_cat_key == "CAT005":
                    share_house = unresolved_sub_property_data.pop("share_house")
                    resolved_sub_property_serializer = prop_serializers.ShareHouseCreateBasicSerializer(data=share_house)
                elif prop_cat_key == "CAT006":
                    commercial_property = unresolved_sub_property_data.pop("commercial_property")
                    units = commercial_property.pop("units")
                    resolved_sub_property_serializer = prop_serializers.CommercialPropertyCreateBasicSerializer(data=commercial_property)
                    units_serializer = prop_serializers.CommercialPropertyUnitCreateBasicSerializer(data=units, many=True)
                elif prop_cat_key == "CAT007":
                    office = unresolved_sub_property_data.pop("office")
                    resolved_sub_property_serializer = prop_serializers.OfficeCreateBasicSerializer(data=office)
                elif prop_cat_key == "CAT008":
                    hall = unresolved_sub_property_data.pop("hall")
                    resolved_sub_property_serializer = prop_serializers.HallCreateBasicSerializer(data=hall)
                elif prop_cat_key == "CAT009":
                    land = unresolved_sub_property_data.pop("land")
                    resolved_sub_property_serializer = prop_serializers.LandCreateBasicSerializer(data=land)
                elif prop_cat_key == "CAT010":
                    all_purpose_property = unresolved_sub_property_data.pop("all_purpose_property")
                    units = all_purpose_property.pop("units")
                    resolved_sub_property_serializer = prop_serializers.AllPurposePropertyCreateBasicSerializer(data=all_purpose_property)
                    units_serializer = prop_serializers.AllPurposePropertyUnitCreateBasicSerializer(data=units, many=True)

                parent_property_serializer = prop_serializers.PropertyCreateBasicSerializer(data=request.data)

                if parent_property_serializer.is_valid():
                    # print("HEYYYY! PROP IS VALID!")
                    property_instance = parent_property_serializer.save(agent=agent_instance, address=property_address_instance, property_category=property_category_instance)
                    # print("HEYYYY! PROP IS STILL VALID!")

                    if resolved_sub_property_serializer is not None:
                        # print("apartment_units: ", apartment)
                        # apartment_units = apartment.pop("units")

                        # apartment_serializer = prop_serializers.ApartmentCreatBasicSerializer(data=apartment)

                        if resolved_sub_property_serializer.is_valid():
                            # print("HEYYYY! APARTMENT IS VALID!")
                            sub_property_instance = resolved_sub_property_serializer.save(property=property_instance)
                            
                            print("apartment_units: ", units)

                            if units_serializer is not None:
                                
                                # units_serializer = prop_serializers.ApartmentUnitCreateBasicSerializer(data=apartment_units, many=True)
                                if units_serializer.is_valid():
                                    print("AFTER UNIT SERIALIZER IS VALID")
                                    if prop_cat_key == "CAT001":
                                        units_serializer.save(apartment=sub_property_instance)
                                    elif prop_cat_key == "CAT006":
                                        units_serializer.save(commercial_property=sub_property_instance)
                                    elif prop_cat_key == "CAT010":
                                        units_serializer.save(all_purpose_property=sub_property_instance)

                                    return Response(data=parent_property_serializer.data, status=status.HTTP_201_CREATED)
                                else:
                                    print("UNIT: ", units_serializer.data)
                                    print("Bad property unit data!")
                                    return Response(data="Bad property unit data!", status=status.HTTP_400_BAD_REQUEST)  
                            return Response(data=parent_property_serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            print("Bad sub-property data!")
                            return Response(data="Bad sub-property data!", status=status.HTTP_400_BAD_REQUEST)
                else: 
                    print("Bad property data!")
                    return Response(data="Bad property data!", status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Something wrong when saving Address!")
                return Response(data="Something wrong when saving Address!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Bad property address data!")
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

class PropertyImageListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    parser_clasess = [MultiPartParser, FormParser]
    permission_classes = [AllowAny,]

    # def get_queryset(self):
    #     return prop_models.PropertyImage.objects.all()
    
    def post(self, request, format=None):
        # print("======REQUEST=====: ",request.data)
        imageData = request.data
        propertyId = imageData.pop("property")
        # print("======PROPID=====: ", propertyId)
        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId[0])
        except ObjectDoesNotExist:
            print("Property is not found!")
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        
        property_image_serializer = prop_serializers.PropertyImageSerializer(data=imageData, context={"request": request})

        if property_image_serializer.is_valid():
            property_image_instance = property_image_serializer.save(property=property_instance)
            print("CREATED!!!!!!!!!!!!!!")
            return Response(data=property_image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Property Image is not valid!")
            return Response(data="Property Image is not valid!", status=status.HTTP_400_BAD_REQUEST)


class PropertyVideoListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyVideo.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    parser_clasess = [MultiPartParser, FormParser]
    permission_classes = [AllowAny,]

    # def get_queryset(self):
    #     return prop_models.PropertyImage.objects.all()
    
    def post(self, request, format=None):
        # print("======REQUEST=====: ",request.data)
        VideoData = request.data
        propertyId = VideoData.pop("property")
        # print("======PROPID=====: ", propertyId)
        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId[0])
        except ObjectDoesNotExist:
            print("Property is not found!")
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        
        property_video_serializer = self.get_serializer(data=VideoData, context={"request": request})

        if property_video_serializer.is_valid():
            property_video_instance = property_video_serializer.save(property=property_instance)
            print("CREATED!!!!!!!!!!!!!!")
            return Response(data=property_video_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Property Video is not valid!")
            return Response(data="Property Video is not valid!", status=status.HTTP_400_BAD_REQUEST)

#=====================================================================================================================
class PropertyImageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    permission_classes = [AllowAny,]

class PropertyVideoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyVideo.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    permission_classes = [AllowAny,]


#=====================================================================================================================
class PropertyFileLabelListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyFileLabel.objects.all()
    serializer_class = prop_serializers.PropertyFileLabelSerializer
    permission_classes = [AllowAny,]