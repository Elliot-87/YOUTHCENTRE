from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Vacancy, JobSeeker, Application,
    AdvisoryCategory, AdvisoryArticle,
    ReferralPartner, ReferralRequest
)

# Custom Admin Site Header
admin.site.site_header = "JobCentre Administration"
admin.site.site_title = "JobCentre Admin Portal"
admin.site.index_title = "Welcome to JobCentre Admin Portal"


# === VACANCY ADMIN ===


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'is_upload_only', 'posted_date', 'closing_date', 'is_active')
    list_filter = ('is_upload_only', 'is_active', 'job_type', 'currency')
    search_fields = ('title', 'company', 'location', 'description')
    readonly_fields = ('posted_date',)

    fieldsets = (
        ('Job Info', {
            'fields': ('title', 'company', 'description', 'location', 'salary', 'salary_min', 'salary_max', 'currency', 'job_type')
        }),
        ('Job Meta', {
            'fields': ('requirements', 'benefits', 'application_email', 'application_url', 'is_featured', 'is_active', 'posted_date', 'closing_date')
        }),
        ('Upload Job Card', {
            'fields': ('is_upload_only', 'attachment')
        }),
    )

    def save_model(self, request, obj, form, change):
        # If is_upload_only is True, clear manual fields
        if obj.is_upload_only:
            obj.title = ''
            obj.company = ''
            obj.description = ''
            obj.location = ''
            obj.salary = ''
        super().save_model(request, obj, form, change)




    def attachment_preview(self, obj):
        if not obj.attachment:
            return "-"
        url = obj.attachment.url
        if obj.is_pdf:
            return format_html('<a href="{}" target="_blank">📄 View PDF</a>', url)
        elif obj.is_image:
            return format_html('<img src="{}" style="max-width:200px;height:auto;" />', url)
        return format_html('<a href="{}" target="_blank">Download</a>', url)

    attachment_preview.short_description = "Attachment Preview"

    # Custom actions
    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive']

    @admin.action(description="Mark selected vacancies as featured")
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Remove featured status")
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)

    @admin.action(description="Mark selected vacancies as active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected vacancies as inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


# === JOB SEEKER ADMIN ===
@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'skills_preview', 'applications_count')
    search_fields = (
        'user__username', 'user__email', 'user__first_name',
        'user__last_name', 'skills', 'experience'
    )
    list_filter = ('user__date_joined',)

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    def skills_preview(self, obj):
        return obj.skills[:50] + '...' if len(obj.skills) > 50 else obj.skills
    skills_preview.short_description = 'Skills'

    def applications_count(self, obj):
        return obj.application_set.count()
    applications_count.short_description = 'Applications'


# === APPLICATION ADMIN ===
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'vacancy', 'applied_date', 'status', 'status_badge')
    list_filter = ('status', 'applied_date', 'vacancy__company')
    search_fields = ('job_seeker__user__username', 'vacancy__title', 'vacancy__company')
    date_hierarchy = 'applied_date'
    list_editable = ('status',)

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'reviewed': 'blue',
            'accepted': 'green',
            'rejected': 'red'
        }
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'


# === ADVISORY CATEGORY ADMIN ===
@admin.register(AdvisoryCategory)
class AdvisoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'articles_count', 'description_preview')
    search_fields = ('name', 'description')

    def description_preview(self, obj):
        return obj.description[:75] + '...' if len(obj.description) > 75 else obj.description
    description_preview.short_description = 'Description'

    def articles_count(self, obj):
        return obj.advisoryarticle_set.count()
    articles_count.short_description = 'Articles'


# === ADVISORY ARTICLE ADMIN ===
@admin.register(AdvisoryArticle)
class AdvisoryArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'is_published', 'read_time')
    list_filter = ('category', 'is_published', 'published_date')
    search_fields = ('title', 'content', 'author', 'excerpt')
    list_editable = ('is_published',)
    date_hierarchy = 'published_date'
    readonly_fields = ('published_date',)

    fieldsets = (
        ('Content', {'fields': ('title', 'category', 'content', 'excerpt')}),
        ('Media', {'fields': ('featured_image',)}),
        ('Publication', {'fields': ('author', 'is_published', 'published_date')}),
    )

    def read_time(self, obj):
        word_count = len(obj.content.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min"
    read_time.short_description = 'Read Time'

    actions = ['publish_articles', 'unpublish_articles']

    @admin.action(description="Publish selected articles")
    def publish_articles(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected articles")
    def unpublish_articles(self, request, queryset):
        queryset.update(is_published=False)


# === REFERRAL PARTNER ADMIN ===
@admin.register(ReferralPartner)
class ReferralPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'phone', 'email', 'referrals_count', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description', 'contact_info', 'phone', 'email')
    list_editable = ('is_active',)

    fieldsets = (
        ('Basic Information', {'fields': ('name', 'category', 'description')}),
        ('Contact Information', {'fields': ('phone', 'email', 'website', 'address')}),
        ('Additional Info', {'fields': ('contact_info', 'is_active')}),
    )

    def referrals_count(self, obj):
        return obj.referralrequest_set.count()
    referrals_count.short_description = 'Referrals'


# === REFERRAL REQUEST ADMIN ===
@admin.register(ReferralRequest)
class ReferralRequestAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'partner', 'requested_date', 'status', 'status_badge')
    list_filter = ('status', 'requested_date', 'partner__category')
    search_fields = ('job_seeker__user__username', 'partner__name', 'reason')
    date_hierarchy = 'requested_date'
    list_editable = ('status',)
    readonly_fields = ('requested_date',)

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'contacted': 'blue',
            'approved': 'green',
            'completed': 'purple',
            'rejected': 'red'
        }
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
