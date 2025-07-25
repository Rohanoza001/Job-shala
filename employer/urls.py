from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.employer_signup, name='employer_signup'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('approval-status/', views.approval_status, name='employer_approval_status'),
    path('jobs/', views.employer_jobs, name='employer_jobs'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('applications/', views.all_applications, name='all_applications'),
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/<int:application_id>/quick-update/', views.quick_status_update, name='quick_status_update'),
    path('messages/', views.employer_messages, name='employer_messages'),
    path('messages/<int:user_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/send/', views.send_message_ajax, name='send_message_ajax'),
]
