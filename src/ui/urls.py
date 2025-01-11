# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("ai-chat/", views.ai_chat, name="ai-chat"),
    path("data-description/", views.data_description, name="data-description"),
    path("data-description/download/", views.data_description_download, name="data-description-download"),
]
