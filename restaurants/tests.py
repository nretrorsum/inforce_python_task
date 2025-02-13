from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from restaurants.models import Restaurant, Menu
from django.utils import timezone
from datetime import timedelta

class RestaurantSerializerValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_restaurant_creation(self):
        response = self.client.post('/restaurants/create/', {
            'name': 'Random Restaurant',
            'address': 'Green Street 34',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'Random Restaurant')

    def test_invalid_phone_number(self):
        response = self.client.post('/restaurants/create/', {
            'name': 'Invalid Phone Restaurant',
            'address': 'Green Street 34',
            'phone_number': '12345'  # Invalid phone number
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
        self.assertEqual(response.data['phone_number'][0], 'Phone number must be at least 10 digits long and contain only numbers.')

    def test_non_numeric_phone_number(self):
        response = self.client.post('/restaurants/create/', {
            'name': 'Non Numeric Phone Restaurant',
            'address': 'Green Street 34',
            'phone_number': '12345abcde'  # Non-numeric phone number
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
        self.assertEqual(response.data['phone_number'][0], 'Phone number must be at least 10 digits long and contain only numbers.')

    def test_empty_address(self):
        response = self.client.post('/restaurants/create/', {
            'name': 'Test Restaurant',
            'address': '',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('address', response.data)
        self.assertEqual(response.data['address'][0], 'This field may not be blank.')


class MenuCreationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Green Street 34',
            phone_number='1234567890'
        )

    def test_valid_menu_creation_today(self):
        response = self.client.post('/restaurants/menu/upload/', {
            'restaurant': self.restaurant.id,
            'date': timezone.now().date(),
            'items': 'Pizza, Pasta'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().restaurant, self.restaurant)

    def test_valid_menu_creation_future_date(self):
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.post('/restaurants/menu/upload/', {
            'restaurant': self.restaurant.id,
            'date': future_date,
            'items': 'Burger, Salad'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().restaurant, self.restaurant)
        
    def test_menu_creation_missing_restaurant(self):
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.post('/restaurants/menu/upload/', {
            'date': future_date,
            'items': 'Tacos, Burritos'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('restaurant', response.data)
        self.assertEqual(response.data['restaurant'][0], 'This field is required.')
        
    def test_menu_creation_past_date(self):
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.post('/restaurants/menu/upload/', {
            'restaurant': self.restaurant.id,
            'date': past_date,
            'items': 'Sushi, Ramen'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        self.assertEqual(
            response.data['date'],
            'Cannot set a menu for a past date. Please select today or a future date.'
        )
