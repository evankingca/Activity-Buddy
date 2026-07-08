from django.contrib import admin
from .models import Activity, UserActivity, Preference
from .models import User
from .models import Connection, DirectMessage

admin.site.register(Connection)
admin.site.register(DirectMessage)
admin.site.register(User)
admin.site.register(Activity)
admin.site.register(UserActivity)
admin.site.register(Preference)
