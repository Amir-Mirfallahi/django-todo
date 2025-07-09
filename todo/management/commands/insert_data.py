import random

from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from todo.models import Task
from datetime import datetime


class Command(BaseCommand):
    help = "Inserting 5 dummy tasks to database"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password="Test@1234")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=4)
        profile.save()

        for _ in range(5):
            Task.objects.create(
                user=user,
                title=self.fake.paragraph(nb_sentences=1),
                description=self.fake.paragraph(nb_sentences=3),
                status=random.choice([False, True]),
                priority=random.choice([1, 2, 3]),
            )
