from django.views import View
from django.http import HttpResponseRedirect
from add2cal import Add2Cal
import datetime
from django.http import (
    JsonResponse,
    HttpResponse
)

DATE_FORMAT = "%Y%m%dT%H%M%S"


class CalendarReminderView(View):

    view_name = 'calendar_reminder_view'

    def get(self, request, *args, **kwargs):
        params = self.request.GET
        start = params.get('start', datetime.datetime.now().strftime(
            DATE_FORMAT))
        end = params.get('end', datetime.datetime.now().strftime(DATE_FORMAT))
        title = params.get('title', 'new reminder')
        description = params.get('description', '')
        location = params.get('location', 'Boston, MA')
        link_type = params.get('link_type', 'data')

        add2cal = Add2Cal(
            start=start,
            end=end,
            title=title,
            description=description,
            location=location)
        calendar_data = add2cal.as_dict()
        if link_type == 'ical':
            response = HttpResponse(
                calendar_data['ical_content'], content_type='text/calendar')
            attachment = 'attachment; filename={title}.ics'.format(
                title=title)
            response['Content-Type'] = 'text/calendar'
            response[
                'Content-Disposition'] = attachment
            return response
        elif link_type == 'outlook':
            return HttpResponseRedirect(
                redirect_to=calendar_data['outlook_link'])
        elif link_type == 'google':
            return HttpResponseRedirect(
                redirect_to=calendar_data['gcal_link'])
        elif link_type == 'yahoo':

            return HttpResponseRedirect(
                redirect_to=calendar_data['yahoo_link'])
        else:
            return JsonResponse(add2cal.as_dict())
