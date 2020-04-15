from impact.v1.views.impact_view import ImpactView



class CancelOfficeHourReservationView(ImpactView):
    view_name = "cancel_office_hours_reservation"
    
    def post(self, request, office_hour_id, message=""):
        requesting_user = request.user
        office_hour = OfficeHour.objects.get(pk=office_hour_id)

         if _can_cancel(requesting_user, office_hour):
             emails = _prepare_email_notifications(office_hour,
                                                   message,
                                                   requesting_user)
             _cancel_reservation(office_hour)
             for email in emails:
                 _send_email(email)

                 
def _can_cancel(user, office_hour):
    return is_staff(user) or user == office_hour.finalist

def _cancel_reservation(office_hour):
    office_hour.finalist = None
    office_hour.save()

def _send_email(email_details):
    email_handler(**email_details).send()

def _prepare_email_notifications(office_hour,
                                 message,
                                 requesting_user):
    pass
        
    
