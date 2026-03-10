from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from common.mixins import ModifyFormData
from drivers.forms import DriverSearchAndSortForm, DriverAddForm, DriverEditForm, DriverDeleteForm
from drivers.mixins import DriverContextMixin
from drivers.models import Driver


class DriverListView(LoginRequiredMixin ,DriverContextMixin,ModifyFormData ,ListView, FormView):
    model = Driver
    template_name = 'driver/drivers-list.html'
    context_object_name = 'drivers'
    form_class = DriverSearchAndSortForm
    paginate_by = 15

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        search_by = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', '')

        if 'search' in self.request.GET:
            queryset = queryset.filter(full_name__icontains=search_by)

        if 'sort' in self.request.GET:
            queryset = queryset.order_by(sort_by)

        return queryset

class DriverDetailView(LoginRequiredMixin,PermissionRequiredMixin, DriverContextMixin, DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related('specializations')
    permission_required = 'drivers.view_driver'
    template_name = 'driver/driver-details.html'


class DriverCreateView(LoginRequiredMixin,PermissionRequiredMixin ,DriverContextMixin, CreateView):
    permission_required = 'drivers.add_driver'
    permission_denied_message = 'Staff only section'
    model = Driver
    queryset = Driver.objects.prefetch_related('specializations')
    template_name = 'driver/driver-create.html'
    form_class = DriverAddForm

    def get_success_url(self) -> str:
        return reverse('driver:details', kwargs={'pk': self.object.pk})


class DriverUpdateView(LoginRequiredMixin,PermissionRequiredMixin ,DriverContextMixin, UpdateView):
    permission_required = 'drivers.change_driver'
    model = Driver
    template_name = 'driver/driver-update.html'
    form_class = DriverEditForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'driver:details'
        context['id'] = self.get_object().pk

        return context

    def get_success_url(self) -> str:
        return reverse('driver:details', kwargs={'pk': self.object.pk})


class DriverDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DriverContextMixin, DeleteView):
    permission_required = 'drivers.delete_driver'
    model = Driver
    template_name = 'driver/driver-delete.html'
    success_url = reverse_lazy('driver:list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'driver:details'
        context['id'] = self.get_object().pk
        context['form'] = DriverDeleteForm(instance=self.object)

        return context