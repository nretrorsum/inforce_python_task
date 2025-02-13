from rest_framework import generics, serializers
from django.utils import timezone
from django.db.models import Count
from .models import Vote
from .serializers import VoteSerializer
from restaurants.models import Restaurant
from restaurants.serializers import  RestaurantSerializer
from rest_framework.permissions import IsAuthenticated
# from utils.version_decorators import check_version

class VoteCreateView(generics.CreateAPIView):
    """
    Allows users to create a vote.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated] #Only authenticated users can vote
    def perform_create(self, serializer):
        user = self.request.user
        today = timezone.now().date()
        if Vote.objects.filter(user=user, date=today).exists():
            raise serializers.ValidationError("You have already voted today.")
        serializer.save(user=user, date=today)        


class TodayMenuResultsView(generics.ListAPIView):
    """
    Provides the results of the votes for the restaurant with the highest votes today.
    """
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        today = timezone.now().date()
        votes = Vote.objects.filter(date=today).values('restaurant').annotate(total_votes=Count('restaurant')).order_by('-total_votes')
        if votes.exists():
            restaurant_id = votes.first()['restaurant']
            return Restaurant.objects.filter(id=restaurant_id)

        return Restaurant.objects.none()
