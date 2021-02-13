"""Security app views."""

from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

CSRF_ERROR_MESSAGE = "Refresh csrf and try again."


class CSRFView(APIView):
  """Provide an endpoint where REST clients can retrieve CSRF tokens."""

  def get(self, request):
    """Respond to authenticated GET requests with a valid CSRF token."""
    token = get_token(request)
    return Response({"token": token}, status=status.HTTP_200_OK)


@api_view([
    'CONNECT',
    'DELETE',
    'GET',
    'HEAD',
    'OPTIONS',
    'POST',
    'PATCH',
    'PUT',
    'TRACE',
])
def csrf_error(request, reason=""):  # pylint: disable=W0613
  """Respond to CSRF error with a 403, and a custom JSON message."""

  return Response(
      {"error": CSRF_ERROR_MESSAGE},
      status=status.HTTP_403_FORBIDDEN,
  )
