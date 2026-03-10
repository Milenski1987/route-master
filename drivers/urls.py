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
    ])),
    path('specializations/', include([
        path('', views.SpecializationsListView.as_view(), name='specializations-list'),
        path('add/', views.SpecializationCreateView.as_view(), name='specialization-add'),
        path('<int:pk>/', include([
            path('', views.SpecializationDetailView.as_view(), name='specialization-details'),
            path('edit/', views.SpecializationUpdateView.as_view(), name='specialization-edit'),
            path('delete/', views.SpecializationDeleteView.as_view(), name='specialization-delete')
        ]))
    ]))
]



