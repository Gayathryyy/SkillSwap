from django.urls import path
from . import views

urlpatterns = [

path(
    'user/<int:user_id>/',
    views.public_profile,
    name='public_profile'
),

    path('', views.my_skills, name='my_skills'),


    path('add/', views.add_skill, name='add_skill'),

    path(
        'edit/<int:skill_id>/',
        views.edit_skill,
        name='edit_skill'
    ),

    path(
        'delete/<int:skill_id>/',
        views.delete_skill,
        name='delete_skill'
    ),

    path(
    'browse/',
    views.browse_skills,
    name='browse_skills'
    ),

]