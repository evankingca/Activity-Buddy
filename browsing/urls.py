from django.urls import path
from . import views
from .views import ConnectionCreateView, ConnectionUpdateView, ConnectionDeleteView

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),

    
    path("profile",views.user_profile, name="user_profile"),

    
    path("user", views.user, name="user"),
    # ------------------------------
    # Auth Endpoints
    # ------------------------------
    path("auth/signup/", views.AuthSignupView.as_view()),
    path("auth/login/", views.AuthLoginView.as_view()),
    path("auth/logout/", views.AuthLogoutView.as_view()),
    path("auth/me/", views.AuthMeView.as_view()),
    # ------------------------------
    # User Endpoints
    # ------------------------------
    path("users/", views.UserListView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view()),
    path("users/<int:pk>/activities/", views.UserActivityListView.as_view()),
    # ------------------------------
    # Activity Endpoints
    # ------------------------------
    path("activities/", views.ActivityListView.as_view()),
    path("activities/<int:pk>/", views.ActivityDetailView.as_view()),
    path("activities/<int:pk>/edit/", views.ActivityUpdateView.as_view()),
    path("activities/create/", views.ActivityCreateView.as_view()),
    path("activities/<int:pk>/delete/", views.ActivityDeleteView.as_view()),
    # ------------------------------
    # UserActivity Endpoints
    # ------------------------------
    path("users/<int:pk>/activities/add/", views.UserActivityCreateView.as_view()),
    path("useractivities/<int:pk>/edit/", views.UserActivityUpdateView.as_view()),
    path("useractivities/<int:pk>/delete/", views.UserActivityDeleteView.as_view()),
    # ------------------------------
    # Preference Endpoints
    # ------------------------------
    path("preferences/", views.PreferenceListCreateView.as_view()),
    path("preferences/<int:pk>/", views.PreferenceDetailView.as_view()),
    path("users/<int:pk>/preferences/", views.UserPreferenceListView.as_view()),

    # ------------------------------
    # Connections Endpoints
    # ------------------------------
    path("connections/", ConnectionCreateView.as_view()),
    path("connections/<int:pk>/", ConnectionUpdateView.as_view()),
    path("connections/<int:pk>/delete/", ConnectionDeleteView.as_view()),

]
