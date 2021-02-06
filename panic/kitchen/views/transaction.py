"""Kitchen Transaction Views"""

import datetime

from django.conf import settings
from django.utils import timezone
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets

from spa_security.mixins import CSRFMixin
from ..filters import TransactionFilter
from ..models.transaction import Transaction
from ..pagination import LegacyTransactionPagination
from ..serializers.transaction import TransactionSerializer
from ..swagger import custom_transaction_view_parm, openapi_ready
from .deprecation import deprecated_warning

TRANSACTION_LIST_SUNSET = datetime.date(year=2021, month=3, day=1)


class TransactionViewSet(
    CSRFMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Transaction API View"""
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.all()
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_class = TransactionFilter
  pagination_class = LegacyTransactionPagination

  def parse_history_querystring(self):
    try:
      return int(
          self.request.GET.get('history', settings.TRANSACTION_HISTORY_MAX)
      )
    except ValueError:
      return int(settings.TRANSACTION_HISTORY_MAX)

  @swagger_auto_schema(
      deprecated=True,
      manual_parameters=[custom_transaction_view_parm],
  )
  def list(self, request, *args, **kwargs):
    return deprecated_warning(
        super().list(request, *args, **kwargs),
        TRANSACTION_LIST_SUNSET,
    )

  @openapi_ready
  def get_queryset(self):
    history = self.parse_history_querystring()

    return self.queryset.filter(
        item__user=self.request.user,
        datetime__date__lte=timezone.now(),
        datetime__date__gt=timezone.now() - datetime.timedelta(days=history)
    ).order_by('-datetime')
