from django.urls import path
from . import views

app_name = "dashboard"          #  namespace registrado

urlpatterns = [
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("admin/", views.dashboard_view,      name="admin_home"),
]
