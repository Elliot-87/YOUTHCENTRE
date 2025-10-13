from django.urls import path
from . import views

app_name = "jobs"  # ✅ must exist exactly like this

urlpatterns = [
    path("", views.vacancy_list, name="vacancy_list"),
    path("<int:pk>/", views.vacancy_detail, name="vacancy_detail"),
    path("", views.job_feed, name="job_feed"),
    path("vacancy/new/", views.create_vacancy, name="create_vacancy"),
    path("vacancy/<int:pk>/", views.vacancy_detail, name="vacancy_detail"),
    path("vacancy/<int:pk>/edit/", views.edit_vacancy, name="edit_vacancy"),
    path("vacancy/<int:pk>/delete/", views.delete_vacancy, name="delete_vacancy"),

    
]


