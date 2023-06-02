from django.conf import settings
from django.db import models


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
  name = models.CharField(max_length=70)
  org = models.ForeignKey(Organization, on_delete=models.CASCADE)

  members = models.ManyToManyField(settings.AUTH_USER_MODEL)

  private = models.BooleanField(default=False)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Topic(models.Model):
  name = models.CharField(max_length=70)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  @property
  def org(self):
    return self.room.org
