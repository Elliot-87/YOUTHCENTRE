from django.core.management.base import BaseCommand
from jobs.models import AdvisoryCategory, ReferralPartner

class Command(BaseCommand):
    help = 'Create sample data for advisory and referrals'
    
    def handle(self, *args, **options):
        self.stdout.write("Starting to create sample data...")
        
        categories_data = [
            {'name': 'Resume Writing', 'icon': 'file', 'description': 'Learn how to create effective resumes and cover letters'},
            {'name': 'Interview Skills', 'icon': 'briefcase', 'description': 'Master interview techniques and preparation strategies'},
            {'name': 'Career Planning', 'icon': 'target', 'description': 'Plan your career path and set professional goals'},
            {'name': 'Job Search Strategies', 'icon': 'search', 'description': 'Effective methods for finding and applying to jobs'},
        ]
        
        for cat_data in categories_data:
            category, created = AdvisoryCategory.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        partners_data = [
            {
                'name': 'Career Training Institute', 'category': 'training',
                'description': 'Professional certification programs', 'phone': '(555) 123-4567',
                'email': 'info@careertraining.edu', 'website': 'https://careertraining.edu',
                'address': '123 Education St, City, State 12345', 'contact_info': 'Contact admissions office'
            },
            {
                'name': 'Financial Aid Office', 'category': 'financial',
                'description': 'Education funding assistance', 'phone': '(555) 234-5678',
                'email': 'finaid@support.org', 'website': 'https://financialaid.org',
                'address': '456 Finance Ave, City, State 12345', 'contact_info': 'Mon-Fri 9am-5pm'
            },
        ]
        
        for partner_data in partners_data:
            partner, created = ReferralPartner.objects.get_or_create(name=partner_data['name'], defaults=partner_data)
            if created:
                self.stdout.write(f'Created partner: {partner.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created!'))
