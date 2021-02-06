"""Exceptions and Exception Handling"""

from django.contrib.admin.utils import flatten
from rest_framework import serializers, status, views


class ValidationPermissionError(serializers.ValidationError):
  default_code = "permission_denied"
  status_code = status.HTTP_403_FORBIDDEN


CUSTOM_VALIDATION_CLASSES = (ValidationPermissionError,)


def kitchen_exception_handler(exc, context):
  """A rest_framework exception handler that manages status codes for custom
  validation errors.

  :param exc: An exception
  :type exc: :class:`BaseException`
  :param context: A dictionary produced by the API view
  :type context: dict

  :returns: A rest_framework response object
  :rtype: :class:`rest_framework.response.Response`
  """
  response = views.exception_handler(exc, context)

  if response is not None:
    handler = CustomValidationExceptionHandler(exc, response)
    handler.process()
    response = handler.response

  return response


class CustomValidationExceptionHandler:
  """Handles custom validation errors that are hidden by DRF.

  :param exc: An exception
  :type exc: :class:`BaseException`
  :param response: A rest_framework response object
  :type response: :class:`rest_framework.response.Response`
  """

  def __init__(self, exc, response):
    self.exc = exc
    self.error_message_list = []
    self.response = response

  def process(self):
    """Processes an exception, and modifies the response if needed."""
    if isinstance(self.exc, serializers.ValidationError):
      self.error_message_list = self.__get_validation_errors()
      self.response = self.__set_status_code()

  def __get_validation_errors(self):
    try:
      return flatten(self.exc.get_full_details().values())
    except AttributeError:
      return []

  def __set_status_code(self):
    for error in self.error_message_list:
      for validator in CUSTOM_VALIDATION_CLASSES:
        if 'code' in error and error['code'] == validator.default_code:
          self.response.status_code = validator.status_code
    return self.response
