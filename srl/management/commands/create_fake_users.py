import requests
import logging
from pytz import UTC
from datetime import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create Fake Users using the randomuser.me API'

    def add_arguments(self, parser):
        parser.add_argument(
            'user_count',
            type=int,
            help='Enter the number of fake user to create'
        )

    def handle(self, *args, **options):
        randomuser_url = 'https://randomuser.me/api/'

        # fields required
        # username
        # first_name
        # last_name
        # email
        # password
        # date_joined

        user_count = options.get('user_count')
        params = {
            'inc': 'email,name,registered,login',
            'password': 'upper,lower,1-16',
            'results': user_count
        }
        response = requests.get(randomuser_url, params)
        data = response.json()
        if data.get('error'):
            error_msg = data.get('error')
            raise CommandError(error_msg)
        else:
            results = data.get('results')
            if results:
                for item in results:
                    email = item.get('email')
                    first_name = item.get('name').get('first')
                    last_name = item.get('name').get('last')
                    date_joined = item.get('registered')
                    username = item.get('login').get('username')
                    password = item.get('login').get('password')

                    # 2014-04-16 16:18:56
                    date_joined = datetime.strptime(date_joined, '%Y-%m-%d %H:%M:%S')
                    date_joined = UTC.localize(date_joined)

                    user_created, created = User.objects.get_or_create(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        password=password,
                        date_joined=date_joined
                    )
                    print('user: {}, created:{}'.format(user_created, created))

        self.stdout.write(self.style.SUCCESS('fake users created'))
