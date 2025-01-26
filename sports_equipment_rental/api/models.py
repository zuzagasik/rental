from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    purchase_date = models.DateField()
    price_per_rental_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    rental_date = models.DateField()
    return_date = models.DateField()
    rental_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name}"

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.rental.user.username} - {self.rental.equipment.name}"
