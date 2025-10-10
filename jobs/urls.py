from django.urls import path
from . import views

app_name = "jobs"  # ✅ must exist exactly like this

urlpatterns = [
    path("", views.vacancy_list, name="vacancy_list"),
    path("<int:pk>/", views.vacancy_detail, name="vacancy_detail"),

    
]
