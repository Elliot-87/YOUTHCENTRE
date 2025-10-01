from django.core.management.base import BaseCommand
from jobs.models import Vacancy





class Command(BaseCommand):
    help = 'Mark some sample jobs as featured'
    
    def handle(self, *args, **options):
        # Get the first few active jobs and mark them as featured
        jobs_to_feature = Vacancy.objects.filter(is_active=True)[:3]
        
        featured_count = 0
        for job in jobs_to_feature:
            if not job.is_featured:
                job.is_featured = True
                job.save()
                featured_count += 1
                self.stdout.write(f'✓ Featured: {job.title} at {job.company}')
        
        if featured_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully featured {featured_count} jobs!'))
        else:
            self.stdout.write('No jobs needed featuring - they are already featured or no jobs exist.')