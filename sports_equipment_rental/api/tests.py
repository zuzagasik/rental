from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Category, Equipment, Rental

class CategoryTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(category.name, 'Test Category')

class EquipmentTestCase(TestCase):
    def test_equipment_creation(self):
        category = Category.objects.create(name='Test Category')
        equipment = Equipment.objects.create(category=category, name='Test Equipment')
        self.assertEqual(equipment.name, 'Test Equipment')

class RentalTestCase(APITestCase):
    def test_rental_creation(self):
        user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        category = Category.objects.create(name='Test Category')
        equipment = Equipment.objects.create(category=category, name='Test Equipment')
        rental = Rental.objects.create(user=user, equipment=equipment, rental_date='2022-01-01', return_date='2022-01-15')
        self.assertEqual(rental.user, user)
        self.assertEqual(rental.equipment, equipment)