from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.serializers import OrgSerializer, RoomSerializer
from chat.models import Organization, Room


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orgs(request):
  orgs = Organization.objects.filter(members=request.user)
  orgs = OrgSerializer(orgs, many=True)
  return Response({"results": orgs.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_rooms(request, org_id):
  if Organization.objects.filter(owners=request.user, id=org_id).count():
    rooms = Room.objects.filter(org__id=org_id)

  else:
    rooms = Room.objects.filter(Q(members=request.user, org__id=org_id) | Q(private=False, org__id=org_id))

  rooms = RoomSerializer(rooms, many=True)
  return Response({"results": rooms.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_rooms(request, org_id):
  rooms = Room.objects.filter(members=request.user, org_id=org_id)
  rooms = RoomSerializer(rooms, many=True)
  return Response({"results": rooms.data})
