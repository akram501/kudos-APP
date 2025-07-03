import uuid
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, db_default="uuid()", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="%(class)s_created_by", on_delete=models.SET_NULL
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="%(class)s_deleted_by", on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class Organization(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "organization"


class User(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "user"

    # Virtual properties for Django auth compatibility
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True  # or implement logic

    @property
    def is_staff(self):
        return False

    @property
    def is_superuser(self):
        return False


class Kudo(BaseModel):
    sender = models.ForeignKey(User, related_name='given_kudos', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_kudos', on_delete=models.CASCADE)
    message = models.TextField()
    given_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}"

    class Meta:
        managed = True
        db_table = "kudo"
        ordering = ['-given_at']
