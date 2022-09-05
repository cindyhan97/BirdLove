from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class petAdoptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = petAdoption
        fields = ['requester','progress','birds']