"""Kitchen App Urls"""

from django.urls import include, path
from rest_framework_extensions.routers import ExtendedSimpleRouter

from . import views

app_name = "kitchen"

router = ExtendedSimpleRouter()
router.register("allitems", views.ListItemsViewSet, basename="allitems")
router.register("shelf", views.ShelfViewSet, basename="shelf")
router.register("store", views.StoreViewSet, basename="store")
router.register("item", views.ItemViewSet, basename="item")
router.register("transaction", views.TransactionViewSet,
                basename="transaction")\
      .register("item",
                views.TransactionQueryViewSet,
                basename="transaction-query",
                parents_query_lookups=['item'])

urlpatterns = [
    path("", include(router.urls)),
]
