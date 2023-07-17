import traceback

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.middleware import AuthenticationMiddleware

import jwt


class JWTAuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    token = request.headers.get('authorization')
    if token:
      try:
        token = token.split()[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

      except:
        traceback.print_exc()

      else:
        user = User.objects.filter(id=payload['user'], is_active=True, profile__version=payload['version']).first()
        if user:
          request.user = user
          request.bypass_csrf = True

    response = self.get_response(request)
    return response


class BypassAuthMiddleware(AuthenticationMiddleware):
  def process_request(self, request):
    if hasattr(request, 'user'):
      return

    return super().process_request(request)
