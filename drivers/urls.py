from django.urls import path, include
from drivers import views


app_name = 'driver'

urlpatterns = [
    path('', views.DriverListView.as_view(), name='list'),
    path('add/', views.DriverCreateView.as_view(), name='add'),
    path('<int:pk>/', include([
        path('', views.DriverDetailView.as_view(), name='details'),
        path('edit/', views.DriverUpdateView.as_view(), name='edit'),
        path('delete/', views.DriverDeleteView.as_view(), name='delete')
    ]))
]



