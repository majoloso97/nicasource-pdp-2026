from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import HelloWorldView

router = DefaultRouter()

urlpatterns = [
    path(
        "hello",
        HelloWorldView.as_view(),
        name="hello-world",
    ),
]

urlpatterns += router.urls
