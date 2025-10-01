from django.core.management.base import BaseCommand
from jobs.models import AdvisoryCategory, ReferralPartner

class Command(BaseCommand):
    help = 'Create sample data for advisory and referrals'
    
    def handle(self, *args, **options):
        self.stdout.write("Starting to create sample data...")
        
        # Create Advisory Categories
        categories_data = [
            {'name': 'Resume Writing', 'icon': 'file', 'description': 'Learn how to create effective resumes and cover letters'},
            {'name': 'Interview Skills', 'icon': 'briefcase', 'description': 'Master interview techniques and preparation strategies'},
            {'name': 'Career Planning', 'icon': 'target', 'description': 'Plan your career path and set professional goals'},
            {'name': 'Job Search Strategies', 'icon': 'search', 'description': 'Effective methods for finding and applying to jobs'},
        ]
        
        for cat_data in categories_data:
            category, created = AdvisoryCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        # Create Referral Partners
        partners_data = [
            {
                'name': 'Career Training Institute',
                'category': 'training',
                'description': 'Professional certification and skill development programs',
                'phone': '(555) 123-4567',
                'email': 'info@careertraining.edu',
                'website': 'https://careertraining.edu',
                'address': '123 Education St, City, State 12345',
                'contact_info': 'Contact our admissions office for program details'
            },
            {
                'name': 'Financial Aid Office', 
                'category': 'financial',
                'description': 'Assistance with education funding and financial planning',
                'phone': '(555) 234-5678',
                'email': 'finaid@support.org',
                'website': 'https://financialaid.org',
                'address': '456 Finance Ave, City, State 12345',
                'contact_info': 'Walk-in hours: Mon-Fri 9am-5pm'
            },
            {
                'name': 'Housing Support Services',
                'category': 'housing', 
                'description': 'Temporary housing assistance and rental support programs',
                'phone': '(555) 345-6789',
                'email': 'housing@community.org',
                'website': 'https://housingsupport.org',
                'address': '789 Shelter Lane, City, State 12345',
                'contact_info': 'Emergency housing available 24/7'
            },
            {
                'name': 'Career Counseling Center',
                'category': 'counseling',
                'description': 'Professional career assessment and guidance services',
                'phone': '(555) 456-7890',
                'email': 'counseling@careercenter.org',
                'website': 'https://careercounseling.org',
                'address': '321 Guidance Blvd, City, State 12345',
                'contact_info': 'Appointments available weekdays'
            },
        ]
        
        for partner_data in partners_data:
            partner, created = ReferralPartner.objects.get_or_create(
                name=partner_data['name'],
                defaults=partner_data
            )
            if created:
                self.stdout.write(f'Created partner: {partner.name}')
            else:
                self.stdout.write(f'Partner already exists: {partner.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))
        self.stdout.write("\nYou can now access:")
        self.stdout.write("  - Advisory section: http://127.0.0.1:8000/advisory/")
        self.stdout.write("  - Referrals section: http://127.0.0.1:8000/referrals/")
        self.stdout.write("  - Admin panel: http://127.0.0.1:8000/admin/")