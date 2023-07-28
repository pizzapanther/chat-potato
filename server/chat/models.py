import json

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import CICharField
from django.db.models.signals import post_save
from django.dispatch import receiver

from asgiref.sync import async_to_sync

from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.admin import NewTopic, KafkaAdminClient


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
  ktopic_created = models.BooleanField(default=False)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ["name", "org"]

  def __str__(self):
    return self.name

  def save(self):
    super().save()

    if not self.ktopic_created:
      create_topic(f'room_{self.id}')
      self.ktopic_created = True
      super().save()


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

  topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

  objects = models.Manager()
  timescale = TimescaleManager()

  def __str__(self):
    return str(self.time)


def create_topic(topic):
  t = NewTopic(name=topic, num_partitions=1, replication_factor=1)
  admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
  admin_client.create_topics(new_topics=[t])
  admin_client.close()


def serializer(value):
  return json.dumps(value).encode()


def deserializer(serialized):
  return json.loads(serialized)

PRODUCER = None

async def get_producer():
  global PRODUCER

  if PRODUCER:
    return PRODUCER

  PRODUCER = AIOKafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=serializer,
    compression_type="lz4"
  )

  await PRODUCER.start()

  return PRODUCER


@async_to_sync
async def send_message_kafka(room_id, text, topic):
  producer = await get_producer()
  await producer.send(f'room_{room_id}', {'text': text, 'topic': topic})


@receiver(post_save, sender=Message, dispatch_uid="kafka_signal")
def kafka_signal(*args, **kwargs):
  msg = kwargs['instance']
  send_message_kafka(msg.topic.room.id, msg.text, msg.topic.name)
