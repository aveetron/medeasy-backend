from django.urls import path
from .views import ProductApiView, ProductDetailsApiView, ReviewApiView, ReviewDetailsApiView

urlpatterns = [
    path("", ProductApiView.as_view()),
    path("details/<str:product_guid>/", ProductDetailsApiView.as_view()),
    path("review/", ReviewApiView.as_view()),
    path("review/<str:review_guid>/", ReviewDetailsApiView.as_view()),
]