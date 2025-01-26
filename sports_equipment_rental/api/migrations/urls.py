from django.urls import path
from .views import RegisterView, LoginView, EquipmentView, RentalView, PaymentView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('equipment/', EquipmentView.as_view()),
    path('rentals/', RentalView.as_view()),
    path('payments/', PaymentView.as_view()),
]
