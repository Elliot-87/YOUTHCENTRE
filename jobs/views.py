from .models import Vacancy, AdvisoryArticle, AdvisoryCategory, ReferralPartner, ReferralRequest
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VacancyForm
from django.contrib.auth.decorators import login_required
from accounts.models import EmployerProfile
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator





def home(request):
    return render(request, 'home.html')

def vacancy_list(request):
    vacancies = Vacancy.objects.all().order_by('-posted_date')
    paginator = Paginator(vacancies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'jobs/vacancy_list.html', {
        'vacancies': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    })


def job_feed(request):
    # timeline-style feed ordered by newest
    vacancies = Vacancy.objects.filter(is_active=True).select_related("employer")
    return render(request, "jobs/feed.html", {"vacancies": vacancies})

def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, "jobs/vacancy_detail.html", {"vacancy": vacancy})

@login_required
def create_vacancy(request):
    # only allowed for approved employers
    try:
        profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return HttpResponseForbidden("You must be an employer to post jobs.")

    if not profile.approved:
        return HttpResponseForbidden("Your employer account is not approved yet.")

    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            vac = form.save(commit=False)
            vac.employer = request.user
            vac.save()
            return redirect("job_feed")
    else:
        form = VacancyForm()
    return render(request, "jobs/vacancy_form.html", {"form": form, "create": True})

@login_required
def edit_vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if vacancy.employer != request.user:
        return HttpResponseForbidden("You can only edit your own vacancy.")
    if request.method == "POST":
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect(vacancy.get_absolute_url())
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, "jobs/vacancy_form.html", {"form": form, "create": False, "vacancy": vacancy})

@login_required
def delete_vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if vacancy.employer != request.user:
        return HttpResponseForbidden("You can only delete your own vacancy.")
    if request.method == "POST":
        vacancy.delete()
        return redirect("job_feed")
    return render(request, "jobs/vacancy_confirm_delete.html", {"vacancy": vacancy})


# ===============================
# 🏠 HOME VIEW
# ===============================
def home(request):
    # Count total active jobs
    total_active_jobs = Vacancy.objects.filter(is_active=True).count()

    # Smart featured jobs logic
    if total_active_jobs == 0:
        featured_vacancies = []
        section_title = "Featured Job Opportunities"
        section_description = "No job opportunities available yet"
    else:
        # Try to get actually featured jobs
        featured_vacancies = Vacancy.objects.filter(is_active=True, is_featured=True).order_by('-posted_date')[:6]

        if featured_vacancies.exists():
            section_title = "Featured Job Opportunities"
            section_description = "Highlighted opportunities from our partner companies"
        else:
            # No featured jobs, fallback to recent
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


# ===============================
# 💼 JOBS
# ===============================
def vacancy_list(request):
    vacancies = Vacancy.objects.filter(is_active=True).order_by('-posted_date')

    # Optional filters
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')

    if job_type:
        vacancies = vacancies.filter(job_type=job_type)
    if location:
        vacancies = vacancies.filter(location__icontains=location)

    context = {
        'vacancies': vacancies,
        'job_types': getattr(Vacancy, 'JOB_TYPES', []),
    }
    return render(request, 'jobs/vacancy_list.html', context)


def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, "jobs/vacancy_detail.html", {"vacancy": vacancy})


# ===============================
# 📰 ADVISORY
# ===============================
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
    articles = AdvisoryArticle.objects.filter(
        category=category,
        is_published=True
    ).order_by('-published_date')
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


# ===============================
# 🤝 REFERRALS
# ===============================
def referrals_home(request):
    categories = ReferralPartner.CATEGORY_CHOICES
    partners = ReferralPartner.objects.filter(is_active=True)

    # Optional category filter
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
    context = {'partner': partner}
    return render(request, 'jobs/referral_partner_detail.html', context)
