from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"Session for {self.user.name}."

class Destination(models.Model):
    name = models.CharField(max_length=255)
    review = models.CharField(max_length=1024)  # this is the users review of the destination
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # some number 1-5
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_publicly = models.BooleanField(default=False)  # allows a user to decide if this destination gets shared with others.

    def __str__(self):
        return f"{self.name} rated {self.rating} by {self.user.name}"