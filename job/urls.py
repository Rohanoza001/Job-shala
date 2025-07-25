from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='job_signup'),
    path('jobs/', views.job_listing, name='job_listing'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('applications/', views.my_applications, name='my_applications'),
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/<int:application_id>/withdraw/', views.withdraw_application, name='withdraw_application'),
    path('dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
]
