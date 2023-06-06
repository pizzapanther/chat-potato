from rest_framework import serializers

from chat.models import Organization


class OrgSerializer(serializers.ModelSerializer):
  class Meta:
    model = Organization
    fields = ['id', 'name', 'slug']
