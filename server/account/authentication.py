from rest_framework.authentication import SessionAuthentication

class FixSessionAuthentication(SessionAuthentication):
  def enforce_csrf(self, request):
    bypass_csrf = getattr(request, 'bypass_csrf', None)
    if bypass_csrf:
      return

    return super().enforce_csrf(request)
