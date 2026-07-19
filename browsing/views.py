from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsSelf

from .models import User, UserActivity, Activity
from .serializers import UserSerializer, UserActivitySerializer, ActivitySerializer, UserActivityWriteSerializer


def index(request):
    context = {}
    return render(request, "browsing/index.html", context)

def register(request):
    context = {}
    return render(request, "browsing/register.html", context)

def login(request):
    context = {}
    return render(request, "browsing/login.html", context)

def user_home(request):
    context = {}
    return render(request, "browsing/user_home.html", context)

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

# /users/{id} POST
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]

# /users/{id}/activities
class UserActivityListView(generics.ListAPIView):
    serializer_class = UserActivitySerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
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
    permission_classes = [IsAuthenticated]

# /activities/{pk}/edit/
class ActivityUpdateView(generics.UpdateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

# /activities/{pk}/delete/
class ActivityDeleteView(generics.DestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]  # or IsAdminUser


# ------------------------------
# UserActivity Views
# ------------------------------
# POST /users/{pk}/activities/add/
class UserActivityCreateView(generics.CreateAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivityWriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.kwargs['pk']
        serializer.save(user_id=user_id)


# PATCH /useractivities/{pk}/edit/
class UserActivityUpdateView(generics.UpdateAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivityWriteSerializer
    permission_classes = [IsAuthenticated]


# DELETE /useractivities/{pk}/delete/
class UserActivityDeleteView(generics.DestroyAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivityWriteSerializer
    permission_classes = [IsAuthenticated]
