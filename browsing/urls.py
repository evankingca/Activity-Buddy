from django.urls import path
from .views import (
    # User views
    UserListView, UserDetailView, UserUpdateView, UserActivityListView,

    # Activity views
    ActivityListView, ActivityDetailView, ActivityUpdateView, ActivityCreateView, ActivityDeleteView,
    UserActivityCreateView, UserActivityUpdateView, UserActivityDeleteView,
)

urlpatterns = [

    # ------------------------------
    # User Endpoints
    # ------------------------------
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/<int:pk>/edit/', UserUpdateView.as_view()),
    path('users/<int:pk>/activities/', UserActivityListView.as_view()),

    # ------------------------------
    # Activity Endpoints
    # ------------------------------
    path('activities/', ActivityListView.as_view()),
    path('activities/<int:pk>/', ActivityDetailView.as_view()),
    path('activities/<int:pk>/edit/', ActivityUpdateView.as_view()),
    path('activities/create/', ActivityCreateView.as_view()),
    path('activities/<int:pk>/delete/', ActivityDeleteView.as_view()),

    # ------------------------------
    # UserActivity Endpoints
    # ------------------------------
    path('users/<int:pk>/activities/add/', UserActivityCreateView.as_view()),
    path('useractivities/<int:pk>/edit/', UserActivityUpdateView.as_view()),
    path('useractivities/<int:pk>/delete/', UserActivityDeleteView.as_view()),

]
