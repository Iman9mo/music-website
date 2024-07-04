from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from music.models import Category, Artist, Song, Comment, Action
from django.utils import timezone
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with lots of data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users
        users = []
        for _ in range(50):
            username = fake.user_name()
            email = fake.email()
            user = User.objects.create_user(username=username, email=email, password='password123')
            users.append(user)
        self.stdout.write(self.style.SUCCESS('Successfully created 50 users'))

        # Create Categories
        categories = []
        for _ in range(10):
            category = Category.objects.create(name=fake.word())
            categories.append(category)
        self.stdout.write(self.style.SUCCESS('Successfully created 10 categories'))

        # Create Artists
        artists = []
        for _ in range(20):
            artist = Artist.objects.create(name=fake.name())
            artists.append(artist)
        self.stdout.write(self.style.SUCCESS('Successfully created 20 artists'))

        # Create Songs
        songs = []
        for _ in range(100):
            song = Song.objects.create(
                title=fake.sentence(nb_words=4),
                artist=random.choice(artists),
                category=random.choice(categories),
                user=random.choice(users),
                likes=random.randint(0, 500),
                views=random.randint(0, 1000),
                approved=random.choice([True, False]),
                file=fake.file_name(category='audio'),
                cover_image=fake.file_name(category='image'),
                created_at=timezone.now()
            )
            songs.append(song)
        self.stdout.write(self.style.SUCCESS('Successfully created 100 songs'))

        # Create Comments
        for _ in range(300):
            Comment.objects.create(
                user=random.choice(users),
                song=random.choice(songs),
                content=fake.text(),
                approved=random.choice([True, False]),
                created_at=timezone.now()
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 300 comments'))

        # Create Actions
        for _ in range(500):
            Action.objects.create(
                user=random.choice(users),
                song=random.choice(songs),
                action_type=random.choice(['play', 'like', 'share']),
                timestamp=timezone.now()
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 500 actions'))
