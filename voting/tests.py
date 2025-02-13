from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from restaurants.models import Restaurant, Menu
from voting.models import Vote

User = get_user_model()

class VotingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@user.com',
            password='test1test',
            first_name='Test',
            last_name='User',
            phone_number='1234567890'
        )
        # Generate JWT token
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Set up necessary data
        self.restaurant = Restaurant.objects.create(
            name='Random Restaurant',
            address='Green Street 34',
            phone_number='1234567890'
        )
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            date='2025-02-13'
        )

    def test_vote_creation(self):
        response = self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vote_already_voted(self):
        self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        response = self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_results(self):
        self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        response = self.client.get('/voting/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vote_results_no_votes(self):
        response = self.client.get('/voting/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
