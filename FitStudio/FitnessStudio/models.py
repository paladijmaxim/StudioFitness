import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.CharField(max_length=1, verbose_name="Gender")
    age = models.IntegerField(verbose_name="Age", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Phone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Tariff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Name tariff")
    price_per_month = models.IntegerField(verbose_name="Price tariff of month")
    is_active = models.BooleanField(default=True, verbose_name="Is active?")

    def __str__(self):
        return f"{self.name}"

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Name club")
    address = models.TextField(verbose_name="Address")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    working_hours = models.TextField(verbose_name="Working hours")
    amenities = models.TextField(verbose_name="Amenities")

    def __str__(self):
        return f"{self.name}"


class UserMembership(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('frozen', 'Frozen'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    tariff_id = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='memberships')
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} {self.tariff_id} {self.start_date} {self.end_date}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_membership_id = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    status = models.BooleanField(default=False, verbose_name="Status")
    amount = models.IntegerField(verbose_name="Amount")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.user_id} {self.user_membership_id}"

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name="Title")
    category = models.CharField(max_length=100, verbose_name="Category")
    duration_minutes = models.IntegerField(verbose_name="Duration")
    level = models.IntegerField(verbose_name="Level")

    def __str__(self):
        return self.title

class Trainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    experience = models.CharField(max_length=150, verbose_name="Experience")
    photo = models.ImageField(
        upload_to='trainers/',
        verbose_name="Photo",
        null=True,
        blank=True,
    )
    speciality = models.CharField(max_length=100, verbose_name="Speciality")

    def __str__(self):
        return self.full_name


class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='events')
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='events')
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    booked_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(verbose_name="Start at")
    end_at = models.DateTimeField(verbose_name="End at")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.class_id} {self.trainer_id} {self.club_id}"

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.event_id} {self.user_id}"

class Trainer_club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='trainer_clubs')
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer_clubs')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    is_active = models.BooleanField(default=True, verbose_name="Is active?")

    def __str__(self):
        return f"{self.club_id} {self.trainer_id}"