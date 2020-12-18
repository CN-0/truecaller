from rest_framework import serializers
from .models import Contact
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
        )


class ContactSerializer(serializers.ModelSerializer):
    contactof = UserSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = (
            'id',
            'contactof',
            'email',
            'name',
            'number'
        )
        depth = 1
