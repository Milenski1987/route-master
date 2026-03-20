from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from typing_extensions import Dict

from accounts.forms import RouteMasterRegisterForm, UserThemeForm
from accounts.models import RouteMasterUserSettings

UserModel = get_user_model()
class UserRegisterView(CreateView):
    form_class = RouteMasterRegisterForm
    model = UserModel
    template_name = 'account/register.html'
    success_url = reverse_lazy('accounts:login')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['theme'] = self.request.user.settings.theme

        return context

class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = RouteMasterUserSettings  # not UserModel
    form_class = UserThemeForm
    template_name = 'account/user-settings.html'

    def get_object(self):
        return self.request.user.settings

    def get_success_url(self):
        return reverse('accounts:settings', kwargs={'pk': self.request.user.pk})