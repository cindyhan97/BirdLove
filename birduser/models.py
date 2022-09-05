

from django.utils.html import escape
from operator import truediv
from random import choices
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models import *
import os 
from django.conf.urls.static import static
from django.utils import timezone
from django.forms.models import BaseModelFormSet
from django.utils.html import format_html


base_path = os.path.dirname(os.path.realpath(__file__))
class adoptionProgressionChoices(models.TextChoices):
    submitted = 'Submitted',
    accepted = 'Accepted',
    looking_for_adopter = 'looking for an adopter',
    transfer_procedures = 'transfering',
    solved = 'solved'
class rescuerPgressionChoices(models.TextChoices):
    submitted = 'submitted',
    accepted = 'accepted',
    in_Progress = 'in_Progress',
    solved = 'solved'

class areaChoices(models.TextChoices):
    north = "North Region",
    east = "East Region"
    ne = "North-East Region",
    central = "Central Region",
    west = "West Region",
    __empty__ = 'Unknown'
    
def user_icon_path(instance, filename):
    return "userAvatar/{0}_{1}".format(instance.user.id, filename)
def user_rescue_request_picture(instance, filename):
    return "userRescue/{0}/{0}_{1}".format(instance.rescue_pk, filename)
def pet_adopt_request_picture(instance, filename):
    return "petAdopt/{0}/{0}_{1}".format(instance.bird.id, filename)

# Create your models here.

class address(models.Model):
    phoneNumber = models.IntegerField(verbose_name= "Mobile Number", null = True, blank = False)
    area = models.CharField(choices= areaChoices.choices, blank=True, default = areaChoices.__empty__, max_length=20)
    postalCode = models.IntegerField(verbose_name= "Postal Code", null = True, blank= False)
    address1 = models.CharField(max_length=50, null = True, blank=False)
    address2 = models.CharField(null = True, blank = True, max_length=50)

class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(null = True, default="", max_length=25)
    avatar = models.ImageField(null = True, blank = True, default ="userAvatar/default-user-icon-8.jpg",
                                                        upload_to = user_icon_path)
    address= models.ForeignKey(address, null=True, blank = True, unique=False, on_delete=models.SET_NULL, related_name="address_user")

class userDonationRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique= False)
    transitionTime = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(null = False)
    success = models.BooleanField(null = False, default=False)
    class Meta:
        ordering = ('-id',)

class anonymousProfile(models.Model):
    nickname = models.CharField(null = False, blank = True, default="", max_length=20)
    address= models.ForeignKey(address, null=True, blank = True, unique=False, on_delete=models.SET_NULL)
    class Meta:
        ordering = ('-id',)

class rescueRequest(models.Model):
    rescueRequester = models.ForeignKey(User, null = True, blank = True, on_delete =models.SET_NULL ,unique=False,default=None, related_name='User_rescueRequest')
    resuceDescription = models.TextField(verbose_name= "More information...", null = True, blank=True)
    requestTime = models.DateTimeField(default = timezone.now)
    progress = models.TextField(choices = rescuerPgressionChoices.choices, default=rescuerPgressionChoices.submitted)
    address= models.ForeignKey(address, null=True, blank = False, unique=False, on_delete=models.SET_NULL)
    class Meta:
        ordering = ('-id',)

class anonymousRequest(models.Model):
    rescueRequester = models.OneToOneField(anonymousProfile, null= True, blank=True, on_delete=models.SET_NULL, default='', related_name='anoUser_request')
    resuceDescription = models.TextField(verbose_name= "More information...", null = True, blank=True)
    requestTime = models.DateTimeField(default = timezone.now)
    class Meta:
        ordering = ('-id',)

class rescueBirdPicture(models.Model):
    rescue_pk = models.ForeignKey(rescueRequest,on_delete=models.SET_NULL,unique=False, null = True, blank = True,default=None, related_name='request_pictures')
    anonymousRequest = models.ForeignKey(anonymousRequest, on_delete=models.SET_NULL, null = True, blank = True, default=None, related_name="rescueRequest", unique=False)
    pict = models.ImageField(upload_to= user_rescue_request_picture, default = '', null = True, blank = True)
    def file_show(self):
        return format_html('<img src = "{}" width= "200px" />',self.pict.url),

class bird(models.Model):
    name = models.CharField(blank= True, null= True, max_length=30)
    species = models.CharField(blank=True, null = True, max_length=30)
    age = models.SmallIntegerField(blank=True, null = True,)
    adoptDescription = models.TextField(verbose_name= "Description", null = True, blank=True)
    applyer = models.ManyToManyField(User, null = True, blank = True)

class petAdoption(models.Model):
    requester = models.ForeignKey(User, null = True, on_delete=models.SET_NULL,unique=False,related_name='user_requester')
    adopter = models.ForeignKey(User, blank=True, null = True, default="", on_delete=models.SET_DEFAULT,unique=False, related_name='User_petAdption')
    progress = models.TextField(choices = adoptionProgressionChoices.choices, default=adoptionProgressionChoices.submitted)
    birds = models.ForeignKey(bird, on_delete=models.DO_NOTHING, related_name="birds_petAdoption",unique=False)
    time = models.TimeField(default=timezone.now, null = True)
    class Meta:
        ordering = ('-id',)

class birdPicture(models.Model):
    bird = models.ForeignKey(bird, on_delete=models.CASCADE, null = True, blank = True, unique= False)
    pict = models.ImageField(upload_to =pet_adopt_request_picture, default = '', null = True, blank = True)

