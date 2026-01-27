from django.urls import path, include
from .views import MeView, SellerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("sellers", SellerViewSet, basename="seller")

urlpatterns = [
    path("me/", MeView.as_view()),
    path("", include(router.urls)),
]

