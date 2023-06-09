from rest_framework import serializers

from account.serializers import PublicViewUserSerializer
from chat.models import Organization, Room, Topic


class OrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = ['id', 'name', 'slug']


class RoomSerializer(serializers.ModelSerializer):
  class Meta:
    model = Room
    fields = ['id', 'name', 'private']


class TopicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Room
    fields = ['id', 'name']
