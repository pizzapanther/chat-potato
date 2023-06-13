from django import forms
from django import http
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse

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
      token  = self.user.profile.temp_token
      return http.HttpResponseRedirect(f"{next}?temp={token}")

  return TemplateResponse(request, 'account_login.html', {'form': form})


@api_view(['POST'])
def get_perm_token(request):
  # auth user with temp token
  user = UserSerializer(user)
  return Response({"user": user.data})


@api_view(['GET'])
def my_details(request):
  if request.user.is_authenticated:
    user = UserSerializer(request.user)
    return Response({"user": user.data})

  return Response({"user": None})
