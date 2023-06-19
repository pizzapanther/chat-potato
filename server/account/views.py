import urllib.parse

from django import forms
from django import http
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse

import jwt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.serializers import UserSerializer


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
  next = forms.CharField(widget=forms.HiddenInput)

  def __init__(self, request, *args, **kwargs):
    self.request = request
    super().__init__(*args, **kwargs)

  def clean(self):
    cleaned = super().clean()

    self.user = authenticate(self.request, username=cleaned['username'], password=cleaned['password'])
    if self.user is None:
      raise ValidationError("Incorrect username or password.")

    return cleaned


def user_login(request):
  if request.method == 'GET':
    form = LoginForm(request, initial=request.GET)

  else:
    form = LoginForm(request, request.POST)

    if form.is_valid():
      token  = form.user.profile.temp_token
      server = urllib.parse.quote(f"{request.scheme}://{request.get_host()}")
      return http.HttpResponseRedirect(f"{form.cleaned_data['next']}?temp={token}&server={server}")

  return TemplateResponse(request, 'account_login.html', {'form': form})


@api_view(['POST'])
def get_perm_token(request):
  token = request.data.get('token')
  if token:
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

    except:
      return http.HttpResponse("Invalid Token", content_type="text/plain", status=400)

    else:
      user = User.objects.filter(id=payload['user'], is_active=True, profile__version=payload['version']).first()
      if user:
        user = UserSerializer(user)
        return Response({"user": user.data})

      return http.HttpResponse("Invalid User", content_type="text/plain", status=400)

  return http.HttpResponse("Token Required", content_type="text/plain", status=400)


@api_view(['GET'])
def my_details(request):
  if request.user.is_authenticated:
    user = UserSerializer(request.user)
    return Response({"user": user.data})

  return Response({"user": None})
