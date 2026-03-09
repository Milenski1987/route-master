from typing import Dict, Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from common.forms import SearchForm
from common.mixins import ModifyFormData
from routes.forms.delivery_points import DeliveryPointDeleteForm, DeliveryPointAddForm, DeliveryPointEditForm
from routes.mixins import DeliveryPointContextMixin
from routes.models import DeliveryPoint


class DeliveryPointListView(LoginRequiredMixin, DeliveryPointContextMixin,ModifyFormData ,ListView, FormView):
    model = DeliveryPoint
    template_name = 'delivery_point/delivery-points-list.html'
    context_object_name = 'delivery_points'
    form_class = SearchForm
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset= super().get_queryset()
        search_by = self.request.GET.get('search', '')

        if search_by:
            queryset = queryset.filter(
                Q(name__icontains=search_by)
                |
                Q(address__icontains=search_by)
                |
                Q(city__icontains=search_by)
            )

        return queryset


class DeliveryPointDetailsView(LoginRequiredMixin, PermissionRequiredMixin ,DeliveryPointContextMixin, DetailView):
    model = DeliveryPoint
    permission_required = 'routes.view_deliverypoint'
    template_name = 'delivery_point/delivery-point-details.html'
    context_object_name = 'delivery_point'


class DeliveryPointCreateView(LoginRequiredMixin, PermissionRequiredMixin , DeliveryPointContextMixin, CreateView):
    permission_required = 'routes.add_deliverypoint'
    model = DeliveryPoint
    form_class = DeliveryPointAddForm
    context_object_name = 'delivery_point'
    template_name = 'delivery_point/delivery-point-create.html'

    def get_success_url(self) -> str:
        return reverse('routes:delivery_point_details', kwargs={'pk': self.object.pk})


class DeliveryPointUpdateView(LoginRequiredMixin, PermissionRequiredMixin, DeliveryPointContextMixin, UpdateView):
    permission_required = 'routes.change_deliverypoint'
    model = DeliveryPoint
    context_object_name = 'delivery_point'
    template_name = 'delivery_point/delivery-point-update.html'
    form_class = DeliveryPointEditForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'routes:delivery_point_details'
        context['id'] = self.get_object().pk

        return context

    def get_success_url(self) -> str:
        return reverse('routes:delivery_point_details', kwargs={'pk': self.object.pk})


class DeliveryPointDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeliveryPointContextMixin, DeleteView):
    permission_required = 'routes.delete_deliverypoint'
    model = DeliveryPoint
    template_name = 'delivery_point/delivery-point-delete.html'
    success_url = reverse_lazy('routes:delivery_points_list')


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'routes:delivery_point_details'
        context['id'] = self.get_object().pk
        context['form'] = DeliveryPointDeleteForm(instance=self.object)

        return context