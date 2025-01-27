from rest_framework import serializers
from .models import User, Equipment, Rental, Payment, Category, Person, Team, Position

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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


class PersonSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(required=True)

    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    
    pseudonim = serializers.CharField(required = False)
    
    def validate_name(self, value):

        if not value.istitle():
            raise serializers.ValidationError(
                "Name should start with a capital letter",
            )
        return value

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.team = validated_data.get('team', instance.team)
        instance.save()
        return instance
    

class PositionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length = 80)
    description = serializers.CharField()
    
    def create(self, validated_data):
        return Position.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nazwa = validated_data.get('name', instance.name)
        instance.opis = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country']
        read_only_fields = ['id']