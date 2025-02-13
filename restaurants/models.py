from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    """
    Represents a restaurant
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Menu(models.Model):
    """
    Represents a menu for a specific restaurant on a specific date
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    items = models.TextField()

    class Meta:
        unique_together = ('restaurant', 'date')

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"
