# File: signups/urls.py
# Purpose:
#   Defines front-end template routes for the VolunteerHub system.
#   These routes render HTML templates. They never expose API data.

from django.urls import path
from . import views

urlpatterns = [

    # Unified authentication page (signup/signin)
    path('auth/', views.unified_auth_page, name='unified-auth'),

    # Student volunteer signup
    path('volunteer-signup/', views.signup_landing_page, name='volunteer-signup'),

    # Coordinator signup
    path('coordinator-signup/', views.coordinator_signup_page, name='coordinator-signup'),

    # Coordinator dashboard
    path('coordinator-dashboard/', views.coordinator_dashboard_page, name='coordinator-dashboard'),

    # Home page after signup
    path("home/", views.home_page, name="home"),

    # Volunteer list page
    path("volunteer-list/", views.volunteer_list_page, name="volunteer-list-page"),

    # Certificate upload page
    path("certificates-page/", views.certificate_upload_page, name="certificate-upload-page"),

    # EmiExplorer Preferences page
    # This must match the name used in the template
    path("preferences/", views.emi_preferences_page, name="emi-preferences-page"),

    # Posts page
    path("posts/", views.posts_list_page, name="posts-list-page"),

    # Create post page
    path("create-post/", views.create_post_page, name="create-post-page"),

    # Edit post page
    path("edit-post/", views.edit_post_page, name="edit-post-page"),

    # Volunteer profile page
    path('volunteer-profile/<int:volunteer_id>/', views.volunteer_profile_page, name='volunteer-profile'),
    
    # Volunteer photo upload page
    path('volunteer-photos/', views.volunteer_photo_upload_page, name='volunteer-photos'),
    
    # Edit profile page (for volunteers)
    path('edit-profile/', views.edit_profile_page, name='edit-profile'),

    # Role creation page (for coordinators)
    path("role-create/", views.role_create_page, name="role-create-page"),

    # Browse opportunities page (for volunteers)
    path("browse-opportunities/", views.browse_opportunities_page, name="browse-opportunities-page"),

    # Email check endpoint for signup/signin logic
    path('check-email/', views.check_user_email, name='check-user-email'),
]
