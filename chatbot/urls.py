from django.urls import path
from .views import index, chatbot_response

urlpatterns = [
    path('',index, name='chatbot-index'),
    path('response/', chatbot_response, name='chatbot-response'),
]