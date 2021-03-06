"""SuggestedItem model."""

from django.db import models

from .mixins import FullCleanMixin
from spa_security.fields import BlondeCharField


class SuggestedItem(
    FullCleanMixin,
    models.Model,
):
  """SuggestItem model."""

  MAXIMUM_NAME_LENGTH = 255

  name = BlondeCharField(max_length=MAXIMUM_NAME_LENGTH, unique=True)

  objects = models.Manager()

  def __str__(self):
    return str(self.name)
