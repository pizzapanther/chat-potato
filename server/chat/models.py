import json

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import CICharField
from django.db.models.signals import post_save
from django.dispatch import receiver

from asgiref.sync import async_to_sync

from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager


class Organization(models.Model):
  name = models.CharField(max_length=70)
  slug = models.SlugField()

  owners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="owned_orgs")
  moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="mod_orgs")
  members = models.ManyToManyField(settings.AUTH_USER_MODEL)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Room(models.Model):
  name = CICharField(max_length=70)
  org = models.ForeignKey(Organization, on_delete=models.CASCADE)

  members = models.ManyToManyField(settings.AUTH_USER_MODEL)

  private = models.BooleanField(default=False)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ["name", "org"]

  def __str__(self):
    return self.name


class Topic(models.Model):
  name = CICharField(max_length=70, db_index=True)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ["name", "room"]

  def __str__(self):
    return self.name

  @property
  def org(self):
    return self.room.org


class Message(models.Model):
  time = TimescaleDateTimeField(interval="10 minutes")

  text = models.TextField(max_length=512)
  morder = models.BigIntegerField()
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

  objects = models.Manager()
  timescale = TimescaleManager()

  class Meta:
    unique_together = ["topic", "morder"]

  def __str__(self):
    return str(self.time)


def msg_serializer(value):
  return json.dumps(value).encode()


def msg_deserializer(serialized):
  return json.loads(serialized)


@receiver(post_save, sender=Message, dispatch_uid="redis_signal")
def redis_signal(*args, **kwargs):
  msg = kwargs['instance']
  prev = Message.objects.filter(topic=msg.topic, morder__lt=msg.morder).order_by('-morder').first()
  if prev:
    prev = prev.morder

  settings.REDIS_CLIENT.publish(
    f'room_{msg.topic.room.id}',
    msg_serializer({
      'id': msg.id,
      'text': msg.text,
      'topic': msg.topic.name,
      'morder': msg.morder,
      'prev': prev,
      'author': msg.author.id,
      'timestamp': msg.time.isoformat()
    })
  )
