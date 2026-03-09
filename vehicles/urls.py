from django.urls import path, include
from vehicles import views


app_name = 'vehicle'

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='list'),
    path('add/', views.VehicleCreateView.as_view(), name='add'),
    path('<int:pk>/', include([
        path('', views.VehicleDetailView.as_view(), name='details'),
        path('edit/', views.VehicleUpdateView.as_view(), name='edit'),
        path('delete/', views.VehicleDeleteView.as_view(), name='delete')
    ]))
]


