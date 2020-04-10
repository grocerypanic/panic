"""Stripped down cookie authenticator."""

from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthentication(JWTAuthentication):
  """The library implementation of this method would fail on a mangled header,
  skipping the cookie check altogether.  I've pulled out the header checks,
  this now strictly checks for the presence of a named cookie.

  This makes auth reliable, even in the presence of header mangling extensions.
  """

  def authenticate(self, request):
    cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
    raw_token = None

    if cookie_name:
      if cookie_name in request.COOKIES:
        raw_token = request.COOKIES.get(cookie_name)

    if not raw_token:
      return None

    validated_token = self.get_validated_token(raw_token)
    return self.get_user(validated_token), validated_token