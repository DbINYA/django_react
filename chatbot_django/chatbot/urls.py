from django.urls import path
from .views import *


urlpatterns = [
    path('chat', chatbot_answer, name="chatbot_url"),
    path('delete-message/<int:message_id>', delete_message, name='delete_message'),
    path('update-message/<int:message_id>', update_message, name='update_message'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout')
]