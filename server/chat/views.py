from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.serializers import OrgSerializer, UserSerializer
from chat.models import Organization


@api_view(['GET'])
def my_details(request):
  if request.user.is_authenticated:
    user = UserSerializer(request.user)
    return Response({"user": user.data})

  return Response({"user": None})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orgs(request):
  orgs = Organization.objects.filter(members=request.user)
  orgs = OrgSerializer(orgs, many=True)
  return Response({"results": orgs.data})
