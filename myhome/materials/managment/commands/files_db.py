from django.core.management.base import BaseCommand
from django.core.management import call_command

from materials.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Fills data to the DB'

    def handle(self, *args, **options):

        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.all().delete()
        Payment.objects.all().delete()

        course = call_command('loaddata', 'course_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
        lesson = call_command('loaddata', 'lesson_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
        user = call_command('loaddata', 'users_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
        payment = call_command('loaddata', 'payment_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))