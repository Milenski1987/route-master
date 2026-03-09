from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, QuerySet
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from common.forms import SearchForm
from common.mixins import ModifyFormData
from routes.forms.assignments import AssignmentDeleteForm, AssignmentAddForm, AssignmentEditForm
from routes.mixins import AssignmentContextMixin, DeliveryPointContextMixin
from routes.models import Assignment


class AssignmentListView(LoginRequiredMixin, AssignmentContextMixin, ModifyFormData, ListView, FormView):
    model = Assignment
    template_name = 'assignment/assignments-list.html'
    context_object_name = 'assignments'
    form_class = SearchForm
    paginate_by = 6

    def get_queryset(self) -> QuerySet:
        queryset = (
            super().get_queryset()
            .select_related('route', 'driver', 'vehicle')
            .prefetch_related('route__points_for_delivery')
        )

        status = self.request.GET.get('status', 'upcoming')

        if status == 'completed':
            queryset = queryset.filter(assignment_start__lt=now().date())
        else:
            queryset = queryset.filter(assignment_start__gte=now().date())

        search_by = self.request.GET.get('search', '')

        if search_by:
            queryset = queryset.filter(
                Q(route__name__icontains=search_by) |
                Q(route__points_for_delivery__name__icontains=search_by) |
                Q(driver__full_name__icontains=search_by) |
                Q(vehicle__make__icontains=search_by)
            )

        return queryset.order_by(f'{"-" if status == "completed" else ""}assignment_start')


class AssignmentDetailsView(LoginRequiredMixin, PermissionRequiredMixin ,AssignmentContextMixin, DetailView):
    permission_required = 'routes.view_assignment'
    queryset = Assignment.objects.select_related('driver', 'vehicle', 'route').prefetch_related('route__points_for_delivery')
    template_name = 'assignment/assignment-details.html'


class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin ,AssignmentContextMixin, CreateView):
    permission_required = 'routes.add_assignment'
    queryset = Assignment.objects.select_related('driver', 'vehicle', 'route').prefetch_related('route__points_for_delivery')
    template_name = 'assignment/assignment-create.html'
    form_class = AssignmentAddForm

    def get_success_url(self) -> str:
        return reverse('routes:assignment_details', kwargs={'pk': self.object.pk})


class AssignmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin ,AssignmentContextMixin, UpdateView):
    permission_required = 'routes.change_assignment'
    queryset = Assignment.objects.select_related('driver', 'vehicle', 'route').prefetch_related('route__points_for_delivery')
    template_name = 'assignment/assignment-update.html'
    form_class = AssignmentEditForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'routes:assignment_details'
        context['id'] = self.get_object().pk

        return context

    def get_success_url(self) -> str:
        return reverse('routes:assignment_details', kwargs={'pk': self.object.pk})


class AssignmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin ,AssignmentContextMixin, DeleteView):
    permission_required = 'routes.delete_assignment'
    model = Assignment
    template_name = 'assignment/assignment-delete.html'
    success_url = reverse_lazy('routes:assignment_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'routes:assignment_details'
        context['id'] = self.get_object().pk
        context['form'] = AssignmentDeleteForm(instance=self.object)

        return context





