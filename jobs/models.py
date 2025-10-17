from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os






class Vacancy(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vacancies")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.employer.username}"

    def get_absolute_url(self):
        return reverse("vacancy_detail", args=[self.pk])


# ----------------------------
# Helper Validators
# ----------------------------
def validate_file_size(value):
    max_mb = 8
    limit = max_mb * 1024 * 1024
    if value.size > limit:
        raise ValidationError(f"File too large. Size should not exceed {max_mb} MB.")

# ----------------------------
# Job Seeker
# ----------------------------
class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# ----------------------------
# Vacancy (Unified Model for Manual + Upload)
# ----------------------------
class Vacancy(models.Model):

    title = models.CharField(max_length=255)
    attachment = models.FileField(upload_to="vacancy_uploads/", blank=True, null=True)
    # optional helper properties
    @property
    def is_pdf(self):
        return self.attachment and self.attachment.name.lower().endswith(".pdf")
    
    @property
    def is_image(self):
        return self.attachment and self.attachment.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))

    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    CURRENCY_CHOICES = [
        ('ZAR', 'South African Rand (R)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
    ]

    # Core fields
    title = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Salary info
    salary = models.CharField(max_length=100, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='ZAR')

    # Job meta
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    application_email = models.EmailField(blank=True)
    application_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateField(blank=True, null=True)

    # File upload (PDF/Image)
    attachment = models.FileField(
        upload_to='vacancies/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg', 'gif']),
            validate_file_size
        ]
    )

    # Type flag: True = uploaded job only, False = manual job
    is_upload_only = models.BooleanField(default=False)

    # ----------------------------
    # Display helpers
    # ----------------------------
    def __str__(self):
        if self.is_upload_only and self.attachment:
            return f"Uploaded Job: {os.path.basename(self.attachment.name)}"
        return f"{self.title} at {self.company}" if self.title else "Untitled Job"

    def get_absolute_url(self):
        return reverse('jobs:vacancy_detail', kwargs={'pk': self.id})

    def formatted_salary(self):
        """Return formatted salary with ZAR symbol"""
        if self.salary_min and self.salary_max:
            return f"R{self.salary_min:,.0f} - R{self.salary_max:,.0f} per annum"
        elif self.salary:
            if self.salary.startswith('$'):
                return self.salary.replace('$', 'R')
            elif not self.salary.startswith('R'):
                return f"R{self.salary}"
            else:
                return self.salary
        return "Salary negotiable"

    # Attachment helpers
    @property
    def _attachment_ext(self):
        if not self.attachment:
            return ''
        name = os.path.basename(self.attachment.name).lower()
        return os.path.splitext(name)[1].lstrip('.')

    @property
    def is_pdf(self):
        return self._attachment_ext == 'pdf'

    @property
    def is_image(self):
        return self._attachment_ext in ('png', 'jpg', 'jpeg', 'gif')

# ----------------------------
# Job Applications
# ----------------------------
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_seeker} applied for {self.vacancy}"

# ----------------------------
# Advisory Models
# ----------------------------
class AdvisoryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📚')

    def __str__(self):
        return self.name

class AdvisoryArticle(models.Model):
    category = models.ForeignKey(AdvisoryCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    author = models.CharField(max_length=100, default='Career Advisor')
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='advisory/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('advisory_detail', kwargs={'article_id': self.id})

# ----------------------------
# Referral Models
# ----------------------------
class ReferralPartner(models.Model):
    CATEGORY_CHOICES = [
        ('training', 'Training & Education'),
        ('counseling', 'Career Counseling'),
        ('financial', 'Financial Assistance'),
        ('housing', 'Housing Support'),
        ('legal', 'Legal Services'),
        ('health', 'Healthcare'),
        ('childcare', 'Childcare'),
        ('other', 'Other Services'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    contact_info = models.TextField()
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ReferralRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    partner = models.ForeignKey(ReferralPartner, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Referral: {self.job_seeker} -> {self.partner}"
