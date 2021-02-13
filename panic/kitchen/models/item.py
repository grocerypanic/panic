"""Item model."""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now
from naturalsortfield import NaturalSortField

from spa_security.fields import BlondeCharField

User = get_user_model()

TWOPLACES = Decimal(10)**-2
MAXIMUM_QUANTITY = 10000
MINIMUM_QUANTITY = 0
MINIMUM_SHELF_LIFE = 1
MAXIMUM_SHELF_LIFE = 365 * 3
DEFAULT_SHELF_LIFE = 7
MAX_LENGTH = 255


def default_expiry():
  """Calculate the default expiry for an Item.

  :returns: A datetime in the future
  :rtype: :class:`datetime.datetime`
  """
  return now() + timedelta(days=DEFAULT_SHELF_LIFE)


class Item(models.Model):
  """Item model."""

  has_partial_quantities = models.BooleanField(default=False)

  index = NaturalSortField(
      for_field="name",
      max_length=MAX_LENGTH,
  )  # Pagination Index
  name = BlondeCharField(max_length=MAX_LENGTH)
  preferred_stores = models.ManyToManyField('Store')
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.FloatField(
      default=0,
      validators=[
          MinValueValidator(MINIMUM_QUANTITY),
          MaxValueValidator(MAXIMUM_QUANTITY),
      ],
  )
  shelf = models.ForeignKey('Shelf', on_delete=models.CASCADE)
  shelf_life = models.IntegerField(
      default=DEFAULT_SHELF_LIFE,
      validators=[
          MinValueValidator(MINIMUM_SHELF_LIFE),
          MaxValueValidator(MAXIMUM_SHELF_LIFE),
      ],
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  objects = models.Manager()

  # These 3 fields are recalculated on each transaction
  next_expiry_date = models.DateField(default=default_expiry)
  next_expiry_quantity = models.FloatField(
      default=0,
      validators=[
          MinValueValidator(MINIMUM_QUANTITY),
          MaxValueValidator(MAXIMUM_QUANTITY)
      ],
  )
  expired = models.FloatField(
      default=0,
      validators=[
          MinValueValidator(MINIMUM_QUANTITY),
          MaxValueValidator(MAXIMUM_QUANTITY)
      ],
  )

  class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'name'], name='item per user')
    ]
    indexes = [
        models.Index(fields=['index']),
    ]

  def __str__(self):
    return str(self.name)

  # pylint: disable=W0222
  def save(self, *args, **kwargs):
    """Clean and save model."""
    self.full_clean()
    return super(Item, self).save(*args, **kwargs)
