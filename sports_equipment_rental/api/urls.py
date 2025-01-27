from django.urls import path
from . import views
from .views import RegisterView, LoginView, CategoryView, EquipmentView, RentalView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('equipment/', EquipmentView.as_view()),
    path('rentals/', RentalView.as_view()),
    #path('persons/', views.person_list),
    #path('persons/<int:pk>/', views.person_detail),
    path('persons/update/<int:pk>/', views.person_update),
    path('persons/delete/<int:pk>/', views.person_delete),
    path('positions/', views.position_list),
    path('positions/<int:pk>/', views.position_detail),
    path("welcome/", views.welcome_view),
    path("persons_html/", views.person_list_html),
    path("persons_html/<int:id>/", views.person_detail_html),
    path("position/<int:pk>/members/", views.PositionMemberView.as_view()),
    path('api/logout/', views.LogoutView.as_view(), name='api_logout'),
    path('team/<int:pk>/', views.TeamDetail.as_view(),  name='team_detail'),
    path('docs/', views.schema_view),
]