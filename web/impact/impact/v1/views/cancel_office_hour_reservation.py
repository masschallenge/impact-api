from impact.v1.views.impact_view import ImpactView


class CancelOfficeHourReservationView(ImpactView):
    def post(self, request, office_hour_id, message=""):
        requesting_user = request.user
        # office hour is reserved?
        # user can cancel reservation?
        # notify users of cancellation

        
    
