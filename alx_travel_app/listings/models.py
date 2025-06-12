from django.db import models
import uuid

# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField()
    location = models.CharField(max_length=200)
    listing_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_available = models.BooleanField()

    def __str__(self):
        return self.listing_id


class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    guest_name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
    guest_name = models.CharField(max_length=200)
    rating = models.TextField()
    comment = models.TextField()
