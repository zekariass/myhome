import os
from django.db import models
from django.utils import timezone
from agents import models as agnt_models
from commons import models as cmn_models


"""A point of interest category is a category of point of interest near to a property"""
class POICategory(models.Model):
    name = models.CharField(verbose_name='POI category name', max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


DISTANCE_UNIT = [
        ('METER', 'Meter'),
        ('KM', 'Kilo Meter'),
        ('MILE', 'Mile'),
    ]

"""Point of interest is special places or facilities near to a property, such as airports, parks, cinemas, etc"""
class PointOfInterest(models.Model):
    poi_category = models.ForeignKey(POICategory, on_delete=models.SET_NULL, null=True, verbose_name='point of interest category')
    name = models.CharField(verbose_name='point of interest name', max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    distance_from_property = models.FloatField(default=0.00)
    distance_unit = models.CharField(choices=DISTANCE_UNIT, max_length=20, default=DISTANCE_UNIT[1][0])
    added_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

"""Every education facility has a level, such as a nursery, elementary, high school, etc"""
class EdufaLevel(models.Model):
    level = models.CharField(verbose_name='education level', max_length=50, blank=False, null=False)
    grade_start = models.CharField(verbose_name='start of grade', max_length=20, blank=False, null=False)
    grade_end = models.CharField(verbose_name='end of grade', max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.level

"""An education facility is an educational institution near to a property. This allows buyers or 
    tenants of the property to know whether their children can access education suitably"""
class EducationFacility(models.Model):

    OWNERSHIP = [
        ('PRIVATE','Private'),
        ('PUBLIC', 'Public'),
        ('NGO', 'NGO'),
        ('OTHER', 'Other')
    ]

    edufa_level = models.ForeignKey(EdufaLevel, on_delete=models.CASCADE, verbose_name='education facility level')
    name = models.CharField(verbose_name='education facility name', max_length=100, blank=False, null=False)
    ownership = models.CharField(verbose_name='who own the education facility?', max_length=50, 
                choices=OWNERSHIP, default=[OWNERSHIP[1][0]])
    distance_from_property = models.FloatField(verbose_name='how far is from property', default=0.00)
    distance_unit = models.CharField(max_length=20, choices=DISTANCE_UNIT, default=DISTANCE_UNIT[1][0])
    description = models.TextField(blank=True, null=True)
    added_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


"""Each transportation facility has a category, such as public bus station, taxi, train, etc"""
class TransFaCategory(models.Model):

    FACILITY_TYPE = [
        ('BUS_STOP', 'Bus Stop'),
        ('TRAIN_STATION', 'Train Station'),
        ('TRAM_STOP', 'Tram Stop'),
        ('METER_TAXI', 'Meter Taxi'),
        ('OTHER', 'Other')
    ]

    name = models.CharField(verbose_name='transportation facility category name', max_length=100, blank=False, null=False)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPE, default=FACILITY_TYPE[0][0])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


"""Nearest transportation facilities to the property, such as public bus stop, train station, etc"""
class TransportFacility(models.Model):
    trans_fa_category = models.ForeignKey(TransFaCategory, on_delete=models.CASCADE, 
                        verbose_name='transportation facility category')
    name =  models.CharField(verbose_name='transportation facility name', max_length=100, blank=False, null=False)
    distance_from_property = models.FloatField(verbose_name='how far is from property', default=0.00)
    distance_unit = models.CharField(max_length=20, choices=DISTANCE_UNIT, default=DISTANCE_UNIT[1][0])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


"""The amenity category is a category of amenities that a property may have, such as entertainment, cleaning, kitchen, etc"""
class AmenityCategory(models.Model):
    name = models.CharField(verbose_name='category name', max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

"""Amenity is a useful feature of a property that the buyer or tenant may like to have with the property"""
class Amenity(models.Model):
    category = models.ForeignKey(AmenityCategory, related_name='amenities', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='amenity name', max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



"""Each property has category"""
class PropertyCategory(models.Model):
    name = models.CharField(verbose_name='property category name', max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(verbose_name='property category description')
    created_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


"""Property is parent class of all property categories"""
class Property(models.Model):
    property_category= models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, related_name='category_properties', null=True)
    agent = models.ForeignKey(agnt_models.Agent, on_delete=models.CASCADE, null=True, related_name='agent_properties', verbose_name='property agent')
    address = models.OneToOneField(cmn_models.Address, on_delete=models.SET_NULL, verbose_name='property address', null=True)
    is_residential = models.BooleanField(verbose_name='is property for residence?', default=True)
    description = models.TextField(verbose_name='property description', null=True, blank=True)
    added_on = models.DateTimeField(verbose_name='property added on date', default=timezone.now, editable=False)
    education_facility = models.ManyToManyField(EducationFacility, related_name='edu_near_by_properties', through='PropertyEduFacility')
    TransportFacility = models.ManyToManyField(TransportFacility, related_name='tran_near_by_properties', through='PropertyTransFacility')
    Point_of_interest = models.ManyToManyField(PointOfInterest, related_name='poi_near_by_properties', through='PropertyPOI')
    amenity = models.ManyToManyField(Amenity, related_name='linked_properties')

    def __str__(self):
        return 'Category=%s, Agent=%s, Is_residential=%s' % (self.property_category.name, self.agent.name, self.is_residentials)


"""Intermediary table between Property and Education Facility"""
class PropertyEduFacility(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    education_facility = models.ForeignKey(EducationFacility, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=timezone.now, editable=False)


"""Intermediary table between Property and Transport Facility"""
class PropertyTransFacility(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    transport_facility = models.ForeignKey(TransportFacility, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=timezone.now, editable=False)


"""Intermediary table between Property and Point of Interests"""
class PropertyPOI(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    point_of_interest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=timezone.now, editable=False)


"""Apartment"""
class Apartment(Property):
    storey = models.IntegerField(verbose_name='apartment storey level', default=0)
    is_new = models.BooleanField(verbose_name='is property new?', default=False, blank=True)
    
    def __str__(self):
        return 'Apartment on storey %s' % (self.storey)

"""An apartment will have at lest one unit"""
class ApartmentUnit(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='parent apartment', related_name='apartment_units')
    number_of_rooms = models.IntegerField(default=1)
    number_of_bed_rooms = models.IntegerField(default=1)
    number_of_baths = models.IntegerField(default=1)
    area = models.FloatField(default=0.00)
    is_furnished = models.BooleanField(verbose_name='is apartment unit furnished?', default=False)
    is_available = models.BooleanField(verbose_name='is apartment available?', default=True)

    def __str__(self):
        return '%s room and %s bed room apartment' % (self.number_of_rooms, self.number_of_bed_rooms)

"""Condominiums are sort of apartments where many residents live in neighbourhood"""
class Condominium(Property):
    number_of_rooms = models.IntegerField(default=1)
    number_of_bed_rooms = models.IntegerField(default=1)
    storey = models.IntegerField(verbose_name='condominium storey level', default=0)
    num_of_baths = models.IntegerField(default=1)
    area = models.FloatField(default=0.00)
    is_furnished = models.BooleanField(verbose_name='is the condominium furnished?', default=False)
    is_new = models.BooleanField(verbose_name='is the condominium new?', default=False)

    def __str__(self):
        return '%s room and %s bed room condominium' % (self.number_of_rooms, self.number_of_bed_rooms)


"""A villa is a large, detached structure with spacious land surrounding it. It is very luxurious and 
    may include amenities such as a pool, stables, and gardens. A villa is generally home to a single-family,
    in contrast to condos and townhomes that are designed to house multiple families. """
class Villa(Property):
    number_of_rooms = models.IntegerField(default=1)
    number_of_bed_rooms = models.IntegerField(default=1)
    storey = models.IntegerField(verbose_name='How many storey it has', default=0)
    num_of_baths = models.IntegerField(default=1)
    total_coumpound_area = models.FloatField(default=0.00)
    housing_area = models.FloatField(default=0.00)
    is_furnished = models.BooleanField(verbose_name='is the villa furnished?', default=False)
    is_new = models.BooleanField(verbose_name='is the villa new?', default=False)
    
    def __str__(self):
        return '%s room and %s bed room villa' % (self.number_of_rooms, self.number_of_bed_rooms)


"""The office is a property that is used for office purposes"""
class TraditionalHome(Property):
    number_of_rooms = models.IntegerField(default=1)
    number_of_bed_rooms = models.IntegerField(default=1)
    storey = models.IntegerField(verbose_name='Home storey level', default=0)
    num_of_baths = models.IntegerField(default=1)
    area = models.FloatField(default=0.00)
    is_furnished = models.BooleanField(verbose_name='is the home furnished?', default=False)
    is_new = models.BooleanField(verbose_name='is the home new?', default=False)

    def __str__(self):
        return '%s rooms and %s bed room traditional home' % (self.number_of_rooms, self.number_of_bed_rooms)


"""Building type is the type of building that the office or commercial property is part of"""
class BuildingType(models.Model):
    type = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type

"""The office is a property that is used for office purposes"""
class Office(Property):
    building_type = models.ForeignKey(BuildingType, related_name='officess',  
        verbose_name='office building type', on_delete=models.SET_NULL, null=True)
    storey = models.IntegerField(verbose_name='office storey level', default=0)
    number_of_rooms = models.IntegerField(default=1)
    area = models.FloatField(default=0.00)
    is_furnished = models.BooleanField(verbose_name='is the home furnished?', default=False)
    is_new = models.BooleanField(verbose_name='is the office new?', default=False)

    def __str__(self):
        return '%s rooms office' % (self.number_of_rooms)


"""Commercial property is a property that is used for commercial or trading purposes"""
class CommercialProperty(Property):
    building_type = models.ForeignKey(BuildingType, related_name='commercial_properties',  
                    verbose_name='commercial property building type', on_delete=models.SET_NULL, null=True)
    storey = models.IntegerField(verbose_name='commercial property storey level', default=0)
    is_new = models.BooleanField(verbose_name='is the commercial property new?', default=False)


"""Commercial properties may have multiple units. Units are a part of the property to be rented or sold on their own. 
    For instance, a commercial centre may be registered as one commercial property and it then has different units"""
class CommercialPropertyUnit(models.Model):
    commercial_property = models.ForeignKey(CommercialProperty, on_delete=models.CASCADE,
                related_name='single_commercial_units', verbose_name='parent commecrial property')
    number_of_rooms = models.IntegerField(default=1)
    area = models.FloatField(verbose_name='total area of the unit', default=0.00)
    com_prop_unit_description = models.TextField()

    def __str__(self):
        return '%s rooms commercial property' % (self.number_of_rooms)


"""Hall is a wide room used for meetings and various ceremonies"""
class Hall(Property):
    storey = models.IntegerField(verbose_name='Hall storey level', default=0)
    number_of_seats = models.IntegerField(verbose_name='how many seats it has?', default=5)
    total_capacity = models.IntegerField(verbose_name='total capacity including standing', default=5)
    hall_description = models.TextField(null=False, blank=False)

    def __str__(self):
        return '%s seats hall' % (self.number_of_seats)

"""Land properties for sale. This property type is advertised for sale only"""
class Land(Property):
    area = models.FloatField(verbose_name='area of the land', default=0.00) 
    length = models.FloatField(verbose_name='length of the land', default=0.00)
    width = models.FloatField(verbose_name='width of the land', default=0.00)
    has_plan = models.BooleanField(verbose_name='the land has plan?', default=True)
    has_debt = models.BooleanField(verbose_name='the land has unpaid debt?', default=False)

    def __str__(self):
        return '%s area land' % (self.area)


"""Versatile property is all fit property that can be used for commercial purposes, offices, or even for residence"""
class VersatileProperty(Property):
    best_category_for = models.ManyToManyField(PropertyCategory, verbose_name='is is used for?')
    vers_prop_description = models.TextField(blank=True, null=True)


class VersatilePropertyUnit(models.Model):
    storey = models.IntegerField(verbose_name='versatile unit storey level', default=0)
    number_of_rooms = models.IntegerField(default=1)
    area = models.FloatField(default=0.00)
    vers_prop_unit_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s storey versatile versatile unit' % (self.storey)


"""Every category may have a different listing price set by administrators"""
class ListingPriceByCategory(models.Model):
    property_category = models.ForeignKey(PropertyCategory, related_name='category_listing_price', on_delete=models.CASCADE)
    price_label = models.CharField(verbose_name='label (name) for this pricing', max_length=100)
    price = models.FloatField(verbose_name='listing price', default=0.00)
    description = models.TextField(blank=True, null=True)
    Added_on = models.DateTimeField(default=timezone.now, editable=False)
    expired_on = models.DateTimeField(blank=True, null=True)

    @property
    def is_expired(self):
        expired = self.expired_on >= timezone.now
        return expired

    def __str__(self):
        return '%s %d' % (self.property_category.name, self.price)


"""Each category may have a discount for listing set by an administrator"""
class ListingDiscountByCategory(models.Model):
    property_category = models.ForeignKey(PropertyCategory, related_name='category_discount', on_delete=models.CASCADE)
    discount_percentage = models.FloatField(verbose_name='listing discount by percentage', default=0.00)
    discount_fixed = models.FloatField(verbose_name='listing discount fixed', default=0.00)
    description = models.TextField(blank=True, null=True)
    discount_start_on = models.DateTimeField(verbose_name='when the discount starts' ,default=timezone.now, editable=True)
    expired_on = models.DateTimeField(blank=True, null=True)

    @property
    def is_expired(self):
        expired = self.expired_on >= timezone.now
        return expired

    def __str__(self):
        return '%s percentage discount %d, fixed discount %d' % (self.property_category.name, 
            self.discount_percentage, self.discount_fixed)


"""Listing Discount by Category table will contain a unique record at any point in time.
     But the discount may be needed to be stored for report purposes. This table stores discount records"""
class ListingDiscountByCategoryHistory(models.Model):
    property_category = models.ForeignKey(PropertyCategory, related_name='category_discount_history', on_delete=models.CASCADE)
    discount_percentage = models.FloatField(verbose_name='listing discount by percentage', default=0.00)
    discount_fixed = models.FloatField(verbose_name='listing discount fixed', default=0.00)
    description = models.TextField(blank=True, null=True)
    discount_start_on = models.DateTimeField(verbose_name='when the discount starts' ,default=timezone.now, editable=True)
    expired_on = models.DateTimeField(blank=True, null=True)

    @property
    def is_expired(self):
        expired = self.expired_on >= timezone.now
        return expired

    def __str__(self):
        return '%s percentage discount %d, fixed discount %d' % (self.property_category.name, 
            self.discount_percentage, self.discount_fixed)



def get_property_image_name(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"properties/static/media/images/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def get_property_video_name(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"properties/static/media/videos/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def get_property_virtual_file_name(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"properties/static/media/virtuals/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


"""Show up images of a property. A property may have one or more images uploaded"""
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='property image', upload_to=get_property_image_name)
    uploaded_on = models.DateTimeField(default=timezone.now, editable=False)

"""video of the property that is uploaded to the system"""
class PropertyVideo(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    video = models.FileField(verbose_name='property video', upload_to=get_property_video_name)
    uploaded_on = models.DateTimeField(default=timezone.now, editable=False)

"""A virtual video that shows the surrounding of the property in a 3D environment"""
class PropertyVirtualVideo(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    virtual_video = models.FileField(verbose_name='property virtual video', upload_to=get_property_virtual_file_name)
    uploaded_on = models.DateTimeField(default=timezone.now, editable=False)


"""A unique feature is a feature that the property has which is good to attract renters or buyers."""
class PropertyUniqueFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='feature name', max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

"""Rules that need to be obeyed by the buyer or renter after the property is bought or rented"""
class Rule(models.Model):

    STRICTNESS = [
        ('LOWER', 'Lower'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High')
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='rule title', max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    strictness = models.CharField(verbose_name='how strict is the rule?', max_length=100, choices=STRICTNESS, default=STRICTNESS[1][0])

    def __str__(self):
        return self.title