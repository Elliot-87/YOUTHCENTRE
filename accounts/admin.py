from django.contrib import admin
from .models import EmployerProfile, JobseekerProfile

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "approved")
    list_filter = ("approved",)
    search_fields = ("user__username", "company_name")

admin.site.register(JobseekerProfile)
