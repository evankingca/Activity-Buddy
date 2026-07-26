from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .permissions import IsSelf
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
)
from rest_framework.views import APIView
from .models import User, UserActivity, Activity, Preference
from django.contrib.auth.decorators import login_required
from .serializers import (
    UserSerializer,
    UserActivitySerializer,
    ActivitySerializer,
    UserActivityWriteSerializer,
    SignupSerializer,
    LoginSerializer,
    PreferenceSerializer,
    PreferenceWriteSerializer,
)


def index(request):
    context = {}
    return render(request, "browsing/index.html", context)


def register(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("/user")
    return render(request, "browsing/register.html", context)


def login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("/user")
    return render(request, "browsing/login.html", context)


from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def user(request):
    context = {}
    return render(request, "browsing/user_home.html", context)


# -------------------------
# Authentication Views
# -------------------------
# /auth/signup/ POST
class AuthSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        django_login(request, user)

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


# /auth/login/ POST
class AuthLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        django_login(request, user)

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


# /auth/logout/ POST
class AuthLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)

        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )


# /auth/me/ GET
# /auth/me/ PATCH
class AuthMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# -------------------------
# User Views
# -------------------------
# /users/{id}
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# /users/
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# /users/{id} PUT
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]


# /users/{id}/activities
class UserActivityListView(generics.ListAPIView):
    serializer_class = UserActivitySerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return UserActivity.objects.filter(user_id=user_id)


# ------------------------------
# Activity Views
# ------------------------------
# /activities/
class ActivityListView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


# /activities/{pk}/
class ActivityDetailView(generics.RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


# /activities/  (POST)
class ActivityCreateView(generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminUser]


# /activities/{pk}/edit/
class ActivityUpdateView(generics.UpdateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminUser]


# /activities/{pk}/delete/
class ActivityDeleteView(generics.DestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminUser]


# ------------------------------
# UserActivity Views
# ------------------------------
# POST /users/{pk}/activities/add/
class UserActivityCreateView(generics.CreateAPIView):
    serializer_class = UserActivityWriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# PATCH /useractivities/{pk}/edit/
class UserActivityUpdateView(generics.UpdateAPIView):
    serializer_class = UserActivityWriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)


# DELETE /useractivities/{pk}/delete/
class UserActivityDeleteView(generics.DestroyAPIView):
    serializer_class = UserActivityWriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)


# ------------------------------
# Preference Views
# ------------------------------
class PreferenceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Preference.objects.filter(user_activity__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PreferenceWriteSerializer

        return PreferenceSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        gym = Activity.objects.get(name="Gym")

        user_activity, _ = UserActivity.objects.get_or_create(
            user=self.request.user,
            activity=gym,
            defaults={
                "is_active": True,
            },
        )

        if Preference.objects.filter(user_activity=user_activity).exists():
            raise ValidationError(
                "Preferences already exist. Use PATCH to update them."
            )

        serializer.save(user_activity=user_activity)


class PreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Preference.objects.filter(user_activity__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PreferenceWriteSerializer

        return PreferenceSerializer


class UserPreferenceListView(generics.ListAPIView):
    serializer_class = PreferenceSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]

        return Preference.objects.filter(user_activity__user_id=user_id)
