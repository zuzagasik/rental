from django.urls import path
from .views import RegisterView, LoginView, CategoryView, EquipmentView, RentalView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('equipment/', EquipmentView.as_view()),
    path('rentals/', RentalView.as_view()),
]