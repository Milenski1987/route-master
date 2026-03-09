from typing import Dict, Any


class DriverContextMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Driver'
        context['icon'] = 'images/driver_icon.png'
        context['back_url'] = 'driver:list'

        return context