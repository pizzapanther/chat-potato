from rest_framework import serializers

from account.serializers import PublicViewUserSerializer
from chat.models import Organization, Room


class OrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = ['id', 'name', 'slug']


class RoomSerializer(serializers.ModelSerializer):
  members = PublicViewUserSerializer(many=True, read_only=True)

  class Meta:
    model = Room
    fields = ['id', 'name', 'members', 'private']
