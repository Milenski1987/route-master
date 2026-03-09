from typing import Dict, Any


class VehicleContextMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vehicle'
        context['icon'] = 'images/vehicle_icon.png'
        context['back_url'] = 'vehicle:list'

        return context