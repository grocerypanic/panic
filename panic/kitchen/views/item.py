"""Kitchen Item Views"""

import pytz
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from spa_security.mixins import CSRFMixin
from ..filters import ItemFilter
from ..models.item import Item
from ..pagination import PagePagination
from ..serializers.item import ItemConsumptionHistorySerializer, ItemSerializer
from ..swagger import custom_item_consumption_view_parm, openapi_ready


class ItemBaseViewSet(
    CSRFMixin,
):
  """Item Base API View"""
  serializer_class = ItemSerializer
  queryset = Item.objects.all()


class ItemViewSet(
    ItemBaseViewSet,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
  """Item API View"""

  @openapi_ready
  def perform_update(self, serializer):
    """Update a Item"""
    serializer.save(user=self.request.user)


class ItemListCreateViewSet(
    ItemBaseViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
  """Item List and Create API View"""
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_class = ItemFilter
  pagination_class = PagePagination

  @openapi_ready
  def get_queryset(self):
    queryset = self.queryset
    return queryset.filter(user=self.request.user).order_by("index")

  @openapi_ready
  def perform_create(self, serializer):
    """Create a new Item"""
    serializer.save(user=self.request.user)


class ItemConsumptionHistoryViewSet(
    CSRFMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
  """Item Consumption History API View"""
  serializer_class = ItemConsumptionHistorySerializer
  queryset = Item.objects.all()

  @openapi_ready
  @swagger_auto_schema(manual_parameters=[custom_item_consumption_view_parm])
  def retrieve(self, request, *args, **kwargs):
    timezone_query = self.request.GET.get('timezone', pytz.utc.zone)
    instance = self.get_object()
    serializer = self.get_serializer(
        instance,
        data={"timezone": timezone_query},
    )
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)
