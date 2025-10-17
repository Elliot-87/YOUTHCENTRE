from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'accounts'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", LogoutView.as_view(next_page="job_feed"), name="logout"),
    path("profile/", views.profile_view, name="profile"),
]


