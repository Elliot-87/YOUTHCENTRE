from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    approved = models.BooleanField(default=False)  # admin toggles this

    def __str__(self):
        return f"{self.company_name or self.user.username}"

class JobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return self.user.username
