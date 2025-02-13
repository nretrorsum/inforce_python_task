import re
from string import punctuation
from rest_framework.exceptions import ValidationError

class CustomUserValidator:
    """
    Provides custom validation methods for user input, specifically for passwords and phone numbers
    """
    @staticmethod
    def validate_password(password):
        digit, upper, lower, symbol = False, False, False, False
        for char in password:
            if char.isdigit():
                digit = True
            if char.isupper():
                upper = True
            if char.islower():
                lower = True
            if char in punctuation:
                symbol = True
        errors = []
        if len(password) < 8:
            errors.append('Password length should be at least 8 characters.')
        if not digit:
            errors.append('Password should have at least one digit.')
        if not upper:
            errors.append('Password should have at least one uppercase letter.')
        if not lower:
            errors.append('Password should have at least one lowercase letter.')
        if not symbol:
            errors.append('Password should have at least one symbol.')
        if errors:
            raise ValidationError(' '.join(errors))
        return password

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = re.compile(r'^(\+\d{1,3})?(\d{10,12})$')
        if not pattern.match(phone_number):
            raise ValidationError('Invalid phone number')
        return phone_number
