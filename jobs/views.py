from django.shortcuts import render, get_object_or_404
from .models import Vacancy, AdvisoryArticle, AdvisoryCategory, ReferralPartner, ReferralRequest

def home(request):
    # Get total active jobs count
    total_active_jobs = Vacancy.objects.filter(is_active=True).count()

    # Smart featured jobs logic
    if total_active_jobs == 0:
        # No jobs at all
        featured_vacancies = []
        section_title = "Featured Job Opportunities"
        section_description = "No job opportunities available yet"
    else:
        # Try to get ACTUALLY featured jobs first
        featured_vacancies = Vacancy.objects.filter(is_active=True, is_featured=True).order_by('-posted_date')[:6]   

        if featured_vacancies:
            # We have genuinely featured jobs
            section_title = "Featured Job Opportunities"
            section_description = "Highlighted opportunities from our partner companies"
        else:
            # No featured jobs, but we have regular jobs - show recent ones
            featured_vacancies = Vacancy.objects.filter(is_active=True).order_by('-posted_date')[:6]
            section_title = "Recent Job Opportunities"
            section_description = "Latest opportunities from our partner companies"

    context = {
        'featured_vacancies': featured_vacancies,
        'section_title': section_title,
        'section_description': section_description,
        'total_active_jobs': total_active_jobs,
    }
    return render(request, 'jobs/home.html', context)

def vacancy_list(request):
    # Get all active vacancies with filters
    vacancies = Vacancy.objects.filter(is_active=True).order_by('-posted_date')

    # Apply filters
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')

    if job_type:
        vacancies = vacancies.filter(job_type=job_type)
    if location:
        vacancies = vacancies.filter(location__icontains=location)

    context = {
        'vacancies': vacancies,
        'job_types': Vacancy.JOB_TYPES,
    }
    return render(request, 'jobs/vacancy_list.html', context)

def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id, is_active=True)
    context = {'vacancy': vacancy}
    return render(request, 'jobs/vacancy_detail.html', context)

def advisory_home(request):
    categories = AdvisoryCategory.objects.all()
    featured_articles = AdvisoryArticle.objects.filter(is_published=True).order_by('-published_date')[:6]
    context = {
        'categories': categories,
        'featured_articles': featured_articles,
    }
    return render(request, 'jobs/advisory_home.html', context)

def advisory_category(request, category_id):
    category = get_object_or_404(AdvisoryCategory, id=category_id)
    articles = AdvisoryArticle.objects.filter(category=category, is_published=True).order_by('-published_date')      
    context = {
        'category': category,
        'articles': articles,
    }
    return render(request, 'jobs/advisory_category.html', context)

def advisory_detail(request, article_id):
    article = get_object_or_404(AdvisoryArticle, id=article_id, is_published=True)
    related_articles = AdvisoryArticle.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id).order_by('-published_date')[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'jobs/advisory_detail.html', context)

def referrals_home(request):
    categories = ReferralPartner.CATEGORY_CHOICES
    partners = ReferralPartner.objects.filter(is_active=True)

    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        partners = partners.filter(category=category_filter)

    context = {
        'partners': partners,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'jobs/referrals_home.html', context)

def referral_partner_detail(request, partner_id):
    partner = get_object_or_404(ReferralPartner, id=partner_id, is_active=True)
    context = {
        'partner': partner,
    }
    return render(request, 'jobs/referral_partner_detail.html', context)