from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),

    # ------------------------------
    # User Endpoints
    # ------------------------------
    path('users/', views.UserListView.as_view()),
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view()),
    path('users/<int:pk>/activities/', views.UserActivityListView.as_view()),

    # ------------------------------
    # Activity Endpoints
    # ------------------------------
    path('activities/', views.ActivityListView.as_view()),
    path('activities/<int:pk>/', views.ActivityDetailView.as_view()),
    path('activities/<int:pk>/edit/', views.ActivityUpdateView.as_view()),
    path('activities/create/', views.ActivityCreateView.as_view()),
    path('activities/<int:pk>/delete/', views.ActivityDeleteView.as_view()),

    # ------------------------------
    # UserActivity Endpoints
    # ------------------------------
    path('users/<int:pk>/activities/add/', views.UserActivityCreateView.as_view()),
    path('useractivities/<int:pk>/edit/', views.UserActivityUpdateView.as_view()),
    path('useractivities/<int:pk>/delete/', views.UserActivityDeleteView.as_view()),

]
