from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.employer_signup, name='employer_signup'),
]
