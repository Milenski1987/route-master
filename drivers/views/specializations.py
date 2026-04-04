from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet, Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from common.forms import SearchForm
from common.mixins import ModifyFormData
from drivers.forms import SpecializationAddForm, SpecializationEditForm, SpecializationDeleteForm
from drivers.mixins import SpecializationContextMixin
from drivers.models import Specialization


class SpecializationsListView(LoginRequiredMixin , PermissionRequiredMixin, SpecializationContextMixin,ModifyFormData ,ListView, FormView):
    model = Specialization
    permission_required = 'drivers.add_specialization'
    template_name = 'specialization/specializations-list.html'
    context_object_name = 'specializations'
    form_class = SearchForm
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        search_by = self.request.GET.get('search', '')

        if 'search' in self.request.GET:
            queryset = queryset.filter(
                Q(name__icontains=search_by)
                |
                Q(description__icontains=search_by)
            )

        return queryset

class SpecializationDetailView(LoginRequiredMixin,PermissionRequiredMixin, SpecializationContextMixin, DetailView):
    model = Specialization
    permission_required = 'drivers.view_specialization'
    template_name = 'specialization/specialization-details.html'


class SpecializationCreateView(LoginRequiredMixin,PermissionRequiredMixin ,SpecializationContextMixin, CreateView):
    permission_required = 'drivers.add_specialization'
    permission_denied_message = 'Staff only section'
    model = Specialization
    template_name = 'specialization/specialization-create.html'
    form_class = SpecializationAddForm

    def get_success_url(self) -> str:
        return reverse('driver:specializations-list')


class SpecializationUpdateView(LoginRequiredMixin,PermissionRequiredMixin ,SpecializationContextMixin, UpdateView):
    permission_required = 'drivers.change_specialization'
    model = Specialization
    template_name = 'specialization/specialization-update.html'
    form_class = SpecializationEditForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'driver:specializations-list'

        return context

    def get_success_url(self) -> str:
        back = self.request.GET.get('back', '/')
        return reverse('driver:specialization-details', kwargs={'pk': self.object.pk}) + f'?back={back}'


class SpecializationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SpecializationContextMixin, DeleteView):
    permission_required = 'drivers.delete_specialization'
    model = Specialization
    template_name = 'specialization/specialization-delete.html'
    success_url = reverse_lazy('driver:specializations-list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'driver:specializations-list'
        context['form'] = SpecializationDeleteForm(instance=self.object)

        return context