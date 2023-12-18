from django.urls import path
from .views import RegisterAPIView

urlpatterns = [
    path("registration/", RegisterAPIView.as_view()),
]