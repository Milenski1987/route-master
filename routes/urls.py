from django.urls import path, include
from routes import views


app_name = 'routes'

assignments_urls = [
    path('add/', views.AssignmentCreateView.as_view(), name='assignment_add'),
    path('', views.AssignmentListView.as_view(), name='assignment_list'),
    path('<int:pk>/', include([
        path('', views.AssignmentDetailsView.as_view(), name='assignment_details'),
        path('edit/', views.AssignmentUpdateView.as_view(), name='assignment_edit'),
        path('delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
        path('api/generate-document/', views.AssignmentGenerateDocumentView.as_view(), name='generate_document'),
        path('document/', views.AssignmentShowDocumentView.as_view(), name='assignment_document')
    ]))
]

routes_urls = [
    path('add/', views.RouteCreateView.as_view(), name='route_add'),
    path('', views.RouteListView.as_view(), name='routes_list'),
    path('<int:pk>/', include([
        path('', views.RouteDetailsView.as_view(), name='route_details'),
        path('edit/', views.RouteUpdateView.as_view(), name='route_edit'),
        path('delete/', views.RouteDeleteView.as_view(), name='route_delete')
    ]))
]

delivery_points_urls = [
    path('add/', views.DeliveryPointCreateView.as_view(), name='delivery_point_add'),
    path('', views.DeliveryPointListView.as_view(), name='delivery_points_list'),
    path('<int:pk>/', include([
        path('', views.DeliveryPointDetailsView.as_view(), name='delivery_point_details'),
        path('edit/', views.DeliveryPointUpdateView.as_view(), name='delivery_point_edit'),
        path('delete/', views.DeliveryPointDeleteView.as_view(), name='delivery_point_delete')
    ]))
]

urlpatterns = [
    path('assignment/', include(assignments_urls)),
    path('routes/', include(routes_urls)),
    path('delivery-points/', include(delivery_points_urls))
]