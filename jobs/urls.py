from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    # Jobs homepage / list view
    path("", views.vacancy_list, name="vacancy_list"),

    # Job feed (if different view logic)
    path("feed/", views.job_feed, name="job_feed"),

    # Vacancy CRUD
    path("vacancy/new/", views.create_vacancy, name="create_vacancy"),
    path("vacancy/<int:pk>/", views.vacancy_detail, name="vacancy_detail"),
    path("vacancy/<int:pk>/edit/", views.edit_vacancy, name="edit_vacancy"),
    path("vacancy/<int:pk>/delete/", views.delete_vacancy, name="delete_vacancy"),
]
