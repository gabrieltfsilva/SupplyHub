from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("suppliers/", include("suppliers.urls")),
    path("users/", core_views.users, name="users"),
    path("delete-user/<int:user_id>/", core_views.delete_user, name="delete_user"),
    path('accounts/', include('accounts.urls')),
]
