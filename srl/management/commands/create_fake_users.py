import requests
from pytz import UTC
from datetime import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


def create_fake_users(count, verbosity=1):
    randomuser_me = 'https://randomuser.me/api/'
    user_count = count
    params = {
        'inc': 'email,name,registered,login',
        'password': 'upper,lower,1-16',
        'results': user_count
    }
    success = 0
    msg = 0
    response = requests.get(randomuser_me, params)
    data = response.json()
    if data.get('error'):
        error_msg = data.get('error')
        success = 1
        msg = error_msg
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
                # todo: use bulk insert
                user_created, created = User.objects.get_or_create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    date_joined=date_joined
                )
                if created:
                    user_created.set_password(password)

                if verbosity > 1:
                    print('user: {}, created:{}'.format(user_created, created))

    return success, msg


class Command(BaseCommand):
    epilog = 'Create Fake Users using the randomuser.me API'
    description = 'Create Fake Users using the randomuser.me API'
    help = 'Create Fake Users using the randomuser.me API'

    def add_arguments(self, parser):
        parser.add_argument(
            'user_count',
            type=int,
            help='Number of fake users to create'
        )

    def handle(self, *args, **options):
        count = options.get('user_count')
        if count <= 0:
            raise CommandError('Please use only positive numbers greater than 0')

        verbosity = options.get('verbosity', 1)
        result, msg = create_fake_users(count, verbosity)
        if result:
            raise CommandError(msg)
        else:
            self.stdout.write(self.style.SUCCESS('fake users created'))
