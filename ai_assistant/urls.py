


from django.urls import path
from .views import ai_query,chat_ui

app_name = "ai_assistant"

urlpatterns = [
    path("ask/", ai_query),
    path("chat/",chat_ui,name='ai_chat'),
]