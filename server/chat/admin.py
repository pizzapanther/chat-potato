from django.contrib import admin

from chat.models import Organization, Room, Topic, Message


@admin.register(Organization)
class OrgAdmin(admin.ModelAdmin):
  list_display = ('name', 'slug', 'counts', 'modified')
  search_fields = ('name', 'slug')
  raw_id_fields = ['members', 'moderators', 'owners']

  def counts(self, obj):
    if obj:
      return f"Members: {obj.members.count()}, Mods: {obj.moderators.count()}, Owners: {obj.owners.count()}"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
  list_display = ('name', 'org', 'private', 'count', 'modified')
  search_fields = ('name',)
  raw_id_fields = ['members', 'org']

  def count(self, obj):
    if obj:
      return obj.members.count()


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
  list_display = ('name', 'room', 'org', 'modified')
  search_fields = ('name',)
  raw_id_fields = ['room']


@admin.register(Message)
class MsgAdmin(admin.ModelAdmin):
  list_display = ('time', 'topic', 'author')
  raw_id_fields = ['topic', 'author']
