from rest_framework import permissions
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Equipment, Rental, Payment, Category
from .serializers import UserSerializer, EquipmentSerializer, RentalSerializer, PaymentSerializer, CategorySerializer
from .permissions import CustomDjangoModelPermissions
from django.http import HttpResponse, Http404
import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return Response({'token': 'your_token_here'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  # Usuwa sesję użytkownika
        return Response({"message": "Log out successful"})

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RentalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RentalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        rentals = Rental.objects.filter(user=request.user)
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        rental_id = request.data['rental_id']
        amount = request.data['amount']
        rental = Rental.objects.get(id=rental_id)
        payment = Payment(rental=rental, amount=amount, payment_status='paid')
        payment.save()
        return Response({'message': 'Payment successful'})
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        payments = Payment.objects.filter(rental__user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    

schema_view = get_swagger_view(title='Sports Equipment Rental API')


# API Views

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rent_equipment(request):
    serializer = RentalSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        rental = serializer.save()
        return Response({"status": "Rental created", "rental_id": rental.id}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_equipment(request):
    try:
        equipments = Equipment.objects.filter(available=True)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rental_history(request):
    try:
        rentals = request.user.rentals.all()
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def person_update(request, pk):

    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])    
def person_delete(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST']) 
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])   
def osoba_list(request):
    if request.method == "GET":
        if not request.user.has_perm("api.view_person_other_owner"):
            Persons = Person.objects.filter(Owner = request.user)
        else:
            Persons = Person.objects.all()
        serializer = PersonSerializer(Persons, many = True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','DELETE'])    
def person_details(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    elif request.method == "DELETE":
        person.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def person_search(request, substring):
    persons = Person.objects.filter(name__icontains = substring) | Person.objects.filter(surname__icontains = substring)
    serializer = PersonSerializer(persons, many = True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def position_list(request):
    if request.method == 'GET':
        stanowiska = Stanowisko.objects.all()
        serializer = StanowiskoSerializer(stanowiska, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'DELETE'])
def position_detail(request, pk):
    try:
        position = Position.objects.get(pk=pk)
    except Position.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PositionSerializer(position)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Welcome User! </br>
        Current date and time: {now}.
        </body></html>"""
    return HttpResponse(html)

@login_required
@permission_required('api.view_person')
def person_list_html(request):
    # pobieramy wszystkie obiekty Person z bazy poprzez QuerySet
    persons = Person.objects.all()
    return render(request,
                  "api/person/list.html",
                  {'persons': persons})
    
def person_detail_html(request, id):
    # pobieramy konkretny obiekt Person
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        raise Http404("Object Person with given id does not exist")

    return render(request,
                  "api/person/detail.html",
                  {'person': person})

class PositionMemberView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            position = Position.objects.get(pk=pk)
        except Position.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        person = Person.objects.filter(position = position)
        serializer = PersonSerializer(persons, many = True)
        return Response(serializer.data)
    
class TeamDetail(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    
    def get_queryset(self):
        return Team.objects.all()

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        team = self.get_object(pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)