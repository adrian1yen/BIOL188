from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = 'admin'
            email = ''
            password = 'admin'
            print 'Creating account for {}'.format(username)
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Users exist')