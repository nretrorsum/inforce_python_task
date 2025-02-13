from .models import CustomUser
from .serializers import UserRegisterSerializer
from django.test import TestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserModelTests(TestCase):
    """
    Tests for the custom user model and user manager
    """
    def test_create_user(self):
        email = 'test@user.com'
        password = 'password123'
        user = CustomUser.objects.create_user(email=email, password=password, first_name='Test', last_name='User', phone_number='1234567890')

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email=None, password='password123')

    def test_create_superuser(self):
        email = 'superuser@example.com'
        password = 'password123'
        user = CustomUser.objects.create_superuser(email=email, password=password, first_name='Super', last_name='User', phone_number='1234567890')

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email='superuser@example.com', password='password123', is_staff=False)

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email='superuser@example.com', password='password123', is_superuser=False)



class UserRegisterSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'phone_number': '1234567890'
        }

    def test_valid_registration(self):
        serializer = UserRegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.valid_data['email'])

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPassword123!'
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)
        self.assertEqual(serializer.errors['password2'], ["Password fields didn't match."])

    def test_invalid_password(self):
        data = self.valid_data.copy()
        data['password'] = 'weak'
        data['password2'] = 'weak'
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_email_already_exists(self):
        CustomUser.objects.create_user(
            first_name='Jane',
            last_name='Smith',
            email=self.valid_data['email'],
            phone_number='0984486926',
            password='AnotherStrongPassword123!'
        )
        serializer = UserRegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'], ['This field must be unique.'])

    def test_invalid_phone_number(self):
        data = self.valid_data.copy()
        data['phone_number'] = 'invalid'
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'], ['Invalid phone number'])
