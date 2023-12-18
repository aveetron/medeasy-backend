from django.urls import path
from .views import OrderApiView, OrderDetailsApiView

urlpatterns = [
    path("", OrderApiView.as_view()),
    path("details/<str:order_guid>/", OrderDetailsApiView.as_view()),
]