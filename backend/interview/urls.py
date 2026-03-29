from django.urls import path
from .views import signup, login, get_questions, submit_answer

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('questions/', get_questions),
    path('submit/', submit_answer),
]