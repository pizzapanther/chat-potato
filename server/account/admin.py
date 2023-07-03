from django.contrib import admin

from account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'first_name', 'email')
  search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
  raw_id_fields = ['user']

  def first_name(self, obj):
    if obj:
      return obj.user.first_name

  def last_name(self, obj):
    if obj:
      return obj.user.last_name

  def email(self, obj):
    if obj:
      return obj.user.email
