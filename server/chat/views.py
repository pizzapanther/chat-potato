
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.serializers import OrgSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orgs(request):
  return Response({"message": "Hello, world!"})
