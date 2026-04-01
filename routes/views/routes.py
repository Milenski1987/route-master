from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, QuerySet, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from common.forms import SearchForm
from common.mixins import ModifyFormData
from routes.forms.routes import RouteDeleteForm, RouteAddForm, RouteEditForm
from routes.mixins import RouteContextMixin
from routes.models import Route


class RouteListView(LoginRequiredMixin, RouteContextMixin, ModifyFormData, ListView, FormView):
    model = Route
    template_name = 'route/routes-list.html'
    context_object_name = 'routes'
    form_class = SearchForm
    paginate_by = 15


    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        search_by = self.request.GET.get('search', '')

        if search_by:
            queryset = queryset.filter(
                Q(name__icontains=search_by)
                |
                Q(start_location__icontains=search_by)
                |
                Q(end_location__icontains=search_by)
            )

        return queryset


class RouteDetailsView(LoginRequiredMixin, PermissionRequiredMixin ,RouteContextMixin, DetailView):
    permission_required = 'routes.view_route'
    queryset = Route.objects.prefetch_related('points_for_delivery')
    template_name = 'route/route-details.html'


class RouteCreateView(LoginRequiredMixin,PermissionRequiredMixin ,RouteContextMixin, CreateView):
    permission_required = 'routes.add_route'
    queryset = Route.objects.prefetch_related('points_for_delivery')
    template_name = 'route/route-create.html'
    form_class = RouteAddForm

    def get_success_url(self) -> str:
        return reverse('routes:route_details', kwargs={'pk': self.object.pk})


class RouteUpdateView(LoginRequiredMixin,PermissionRequiredMixin ,RouteContextMixin, UpdateView):
    permission_required = 'routes.change_route'
    queryset = Route.objects.prefetch_related('points_for_delivery')
    template_name = 'route/route-update.html'
    form_class = RouteEditForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'routes:route_details'
        context['id'] = self.get_object().pk

        return context

    def get_success_url(self) -> str:
        return reverse('routes:route_details', kwargs={'pk': self.object.pk})


class RouteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, RouteContextMixin, DeleteView):
    permission_required = 'routes.delete_route'
    model = Route
    template_name = 'route/route-delete.html'
    success_url = reverse_lazy('routes:routes_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['back_url'] = 'routes:route_details'
        context['id'] = self.get_object().pk
        context['form'] = RouteDeleteForm(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            messages.error(request,"Unable to delete: Route has active assignments.")

            return redirect('routes:route_delete', pk=self.object.pk)