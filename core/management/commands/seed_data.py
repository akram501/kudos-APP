from django.core.management.base import BaseCommand
from core.models import Organization, User, Kudo
import random
import uuid
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.db import transaction

fake = Faker()


class Command(BaseCommand):
    help = "Efficiently seeds the database with demo organizations, users, and kudos."

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing data...")
        Kudo.objects.all().delete()
        User.objects.all().delete()
        Organization.objects.all().delete()

        self.stdout.write("Seeding organizations and users...")
        self.seed_organizations_and_users()

        self.stdout.write("Seeding kudos...")
        self.seed_kudos()

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))

    def seed_organizations_and_users(self):
        self.orgs = []
        self.users = []

        org_objs = []
        org_id_to_org = {}
        for _ in range(3):
            org_uuid = uuid.uuid4()
            org = Organization(
                id=org_uuid,
                name=fake.company()
            )
            org_objs.append(org)
            org_id_to_org[org_uuid] = org

        Organization.objects.bulk_create(org_objs)

        user_objs = []
        user_list_per_org = {org_id: [] for org_id in org_id_to_org.keys()}

        # generate user password
        user_pass = make_password('kudos123')

        for i, (org_id, org) in enumerate(org_id_to_org.items()):
            for j in range(5):
                user_uuid = uuid.uuid4()

                if i == 0 and j == 0:
                    # first user of first org
                    user_email = 'kudosuser1@yopmail.com'
                else:
                    user_email = fake.unique.email()

                user = User(
                    id=user_uuid,
                    organization_id=org_id,
                    name=fake.name(),
                    email=user_email,
                    password=user_pass
                )
                user_objs.append(user)
                user_list_per_org[org_id].append(user)

        User.objects.bulk_create(user_objs)

        # Store flat list of users for seeding kudos
        self.users = user_objs
        self.user_list_per_org = user_list_per_org

    def seed_kudos(self):
        messages = [
            "Great job on the project!",
            "Thanks for helping me out!",
            "Really appreciate your effort.",
            "You went above and beyond!",
            "Your work ethic is inspiring!"
        ]

        kudo_objs = []
        for _ in range(20):
            sender = random.choice(self.users)
            # Ensure receiver is from the same organization and not same as sender
            receiver_candidates = [u for u in self.user_list_per_org[sender.organization_id] if u != sender]
            if not receiver_candidates:
                continue
            receiver = random.choice(receiver_candidates)

            kudo = Kudo(
                id=uuid.uuid4(),
                sender=sender,
                receiver=receiver,
                message=random.choice(messages),
                created_by=sender
            )
            kudo_objs.append(kudo)

        Kudo.objects.bulk_create(kudo_objs)
