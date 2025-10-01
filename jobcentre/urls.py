from django.urls import path, include
from django.contrib import admin
from jobs.views import (
    home, vacancy_list, vacancy_detail,
    advisory_home, advisory_category, advisory_detail,
    referrals_home, referral_partner_detail
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("jobs/", vacancy_list, name="vacancy_list"),
    path("jobs/<int:vacancy_id>/", vacancy_detail, name="vacancy_detail"),
    
    # Advisory URLs
    path("advisory/", advisory_home, name="advisory_home"),
    path("advisory/category/<int:category_id>/", advisory_category, name="advisory_category"),
    path("advisory/article/<int:article_id>/", advisory_detail, name="advisory_detail"),
    
    # Referrals URLs
    path("referrals/", referrals_home, name="referrals_home"),
    path("referrals/partner/<int:partner_id>/", referral_partner_detail, name="referral_partner_detail"),
]