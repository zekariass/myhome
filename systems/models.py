from django.db import models
from django.utils import timezone
import os
from django.conf import settings

"""Users can give ratings of their user experience about the system by number rating"""
class SystemRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="system_ratings")
    rating = models.IntegerField(verbose_name="System rating value", default=0)
    rated_on = models.DateTimeField(default=timezone.now, editable=False)

"""Users can write any feedback about the system. Feedback is a comment about their user experience of the system. 
    It allows to improve the system with additional features or modify the existing one"""
class SystemFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="system_feedbacks")
    feedback = models.TextField(verbose_name="System feedback")
    rated_on = models.DateTimeField(default=timezone.now, editable=False)


def get_system_asset_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"systems/static/assets/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


"""The system may be configurable with a variety of assets, such as pictures for logo, slider, etc"""
class SystemAsset(models.Model):
    asset_type = models.CharField(verbose_name="system asset type", max_length=50, unique=True, blank=False, null=False)
    asset_path = models.FileField(verbose_name="asset file path", upload_to=get_system_asset_path)
    asset_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "type: %s, path: %s" % (self.asset_type, self.asset_path)

"""System assets may be owned by a specific page or module"""
class SystemAssetOwner(models.Model):
    asset = models.ManyToManyField(SystemAsset, verbose_name="system asset")
    owner = models.CharField(verbose_name="system owner page or sub-page", max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.owner


"""There might be a variety of parameters we may store so that the system can use them for doing 
    some functionality with it during the listing, such as promotional parameters"""
class ListingParameter(models.Model):
    param_name = models.CharField(verbose_name="listing parameter name", unique=True, blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.param_name


"""System parameters are parameters used by the system for different purposes. Parameters are values that the system 
    use to function well, such as folder names, password length, password expiry age, etc"""
class SystemParameter(models.Model):
    param_name = models.CharField(verbose_name="system parameter name", unique=True, blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.param_name