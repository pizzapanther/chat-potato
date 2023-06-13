from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  jwt = serializers.DictField(source="profile.jwt")

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'jwt']

