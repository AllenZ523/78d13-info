from django.urls import path
from . import views

app_name = 'members_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/members/', views.api_members, name='api_members'),
    path('api/members/add/', views.api_add_member, name='api_add_member'),
    path('api/members/<str:gaijin_id>/update/', views.api_update_member, name='api_update_member'),
    path('api/members/<str:gaijin_id>/delete/', views.api_delete_member, name='api_delete_member'),
]