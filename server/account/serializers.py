from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  jwt = serializers.DictField(source="profile.jwt")

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'jwt']


class PublicViewUserSerializer(serializers.ModelSerializer):
  name = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ['username', 'name']

  def get_name(self, obj):
    if obj.first_name and obj.last_name:
      return obj.first_name + " " + obj.last_name

    if obj.first_name:
      return obj.first_name

    return obj.username
