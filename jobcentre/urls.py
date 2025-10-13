from django.urls import path, include
from django.contrib import admin
from jobs.views import home, advisory_home, advisory_category, advisory_detail
from jobs.views import referrals_home, referral_partner_detail
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),

    # ✅ Jobs URLs are namespaced
    path("jobs/", include(('jobs.urls', 'jobs'), namespace='jobs')),
    path("accounts/", include("accounts.urls")),

    # Advisory URLs
    path("advisory/", advisory_home, name="advisory_home"),
    path("advisory/category/<int:category_id>/", advisory_category, name="advisory_category"),
    path("advisory/article/<int:article_id>/", advisory_detail, name="advisory_detail"),

    # Referrals URLs
    path("referrals/", referrals_home, name="referrals_home"),
    path("referrals/partner/<int:partner_id>/", referral_partner_detail, name="referral_partner_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
