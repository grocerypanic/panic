"""Store model."""

from django.contrib.auth import get_user_model
from django.db import models

from .mixins import FullCleanMixin, UniqueNameConstraintMixin
from naturalsortfield import NaturalSortField
from spa_security.fields import BlondeCharField

User = get_user_model()


class Store(
    FullCleanMixin,
    UniqueNameConstraintMixin,
    models.Model,
):
  """Store model."""

  MAXIMUM_NAME_LENGTH = 255

  name = BlondeCharField(max_length=MAXIMUM_NAME_LENGTH)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  _index = NaturalSortField(
      for_field="name",
      max_length=MAXIMUM_NAME_LENGTH,
  )

  objects = models.Manager()

  class Meta:
    indexes = [
        models.Index(fields=['_index']),
    ]

  def __str__(self):
    return str(self.name)
