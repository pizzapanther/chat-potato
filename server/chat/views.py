from django import http
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from chat.serializers import OrgSerializer, RoomSerializer, TopicSerializer
from chat.models import Organization, Room, Topic, Message


def paginated_reponse(request, serializer, queryset):
  pnum = request.GET.get('page', '1')
  try:
    pnum = int(pnum)

  except:
    raise http.Http404

  pager = Paginator(queryset, api_settings.PAGE_SIZE)
  page = pager.get_page(pnum)

  capn = serializer(page.object_list, many=True)
  page_data = {
    "count": pager.count,
    "num_pages": pager.num_pages,
    "current": pnum,
    "has_next": page.has_next(),
    "has_prev": page.has_previous(),
  }
  return Response({"results": capn.data, "pagination": page_data})


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

  rooms = rooms.order_by('name')
  return paginated_reponse(request, RoomSerializer, rooms)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_rooms(request, org_id):
  rooms = Room.objects.filter(members=request.user, org_id=org_id).order_by('name')
  return paginated_reponse(request, RoomSerializer, rooms)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topic_list(request, org_id, room_id):
  topics = Topic.objects.filter(room__members=request.user, room__org_id=org_id, room_id=room_id).order_by('-modified')
  return paginated_reponse(request, TopicSerializer, topics)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_chat(request, org_id, room_id):
  topic = request.data.get('topic')
  message = request.data.get('message')
  if not topic:
    return http.HttpResponse("Topic Required", content_type="text/plain", status=400)

  if not message:
    return http.HttpResponse("Message Required", content_type="text/plain", status=400)

  room = Room.objects.filter(members=request.user, org_id=org_id, id=room_id).first()
  if not room:
    raise http.Http404

  topic = Topic.objects.filter(room=room, name=topic).first()
  if not topic:
    topic = Topic(name=topic, room=room)
    topic.save()

  for i in range(5):
    morder = Message.objects.filter(topic=topic).order_by('-morder').first()
    if morder:
      morder = morder.morder + 1

    else:
      morder = 1

    try:
      message = Message(
        time=timezone.now(),
        text=message,
        topic=topic,
        author=request.user,
        morder=morder,
      )
      message.save()

    except:
      pass

    else:
      print("New Message POST:", message.id)
      return Response({"results": {"saved": message.id}})

  raise
