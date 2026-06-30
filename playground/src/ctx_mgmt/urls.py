from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ContextAssistantChatView, ContextAssistantSeedView, HelloWorldView

router = DefaultRouter()

urlpatterns = [
    path(
        "hello",
        HelloWorldView.as_view(),
        name="hello-world",
    ),
    path(
        "assistant/chat",
        ContextAssistantChatView.as_view(),
        name="ctx-mgmt-chat",
    ),
    path(
        "assistant/seed",
        ContextAssistantSeedView.as_view(),
        name="ctx-mgmt-seed",
    ),
]

urlpatterns += router.urls
