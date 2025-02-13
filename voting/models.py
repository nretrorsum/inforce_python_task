from django.db import models
from django.conf import settings
from restaurants.models import Restaurant

class Vote(models.Model):
    """
    Represents a vote made by a user for a restaurant's menu on a specific date.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ['user', 'restaurant', 'date']

    def __str__(self):
        return f"{self.user} voted for {self.restaurant} on {self.date}"
