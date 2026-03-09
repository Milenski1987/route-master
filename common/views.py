from django.db.models import Sum
from django.db.models.aggregates import Count
from django.utils.timezone import now
from django.views.generic import TemplateView
from drivers.models import Driver
from routes.models import Route, Assignment
from vehicles.models import Vehicle


class LoggedHomePageView(TemplateView):
    template_name = 'home-page.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        today = now().date()

        context['assignments'] = (Assignment.objects
                                  .filter(assignment_start__lt=today)
                                  .aggregate(assignments_count=Count('pk')))['assignments_count']

        context['mileage'] = (Assignment.objects
                              .select_related('route')
                              .filter(assignment_start__lt=today)
                              .aggregate(mileage=Sum('route__distance_km')))['mileage']

        context['driver'] = (Driver.objects
                         .prefetch_related('driver_assignments')
                         .filter(driver_assignments__assignment_start__lt=today)
                         .annotate(assignment_count=Count('driver_assignments'))
                         .order_by('-assignment_count')
                         .first())

        context['vehicle'] = (Vehicle.objects
                          .prefetch_related('vehicle_assignments')
                          .filter(vehicle_assignments__assignment_start__lt=today)
                          .annotate(assignment_count=Count('vehicle_assignments'))
                          .order_by('-assignment_count')
                          .first())


        return context
