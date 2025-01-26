from rest_framework import serializers
from .models import User, Equipment, Rental, Payment, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'address']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EquipmentSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'category', 'availability', 'purchase_date', 'price_per_rental_day']

class RentalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = ['id', 'user', 'equipment', 'rental_date', 'return_date', 'rental_status']

class PaymentSerializer(serializers.ModelSerializer):
    rental = RentalSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'rental', 'payment_date', 'amount', 'payment_status']
