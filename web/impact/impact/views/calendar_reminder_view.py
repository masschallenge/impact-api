from django.views import View
from django.http import HttpResponseRedirect
from add2cal import Add2Cal
import datetime
from django.http import (
    JsonResponse,
    HttpResponse
)

DATE_FORMAT = "%Y%m%dT%H%M%S"
CALENDAR_CONTENT_TYPE = 'text/calendar'
OUTLOOK_LINK_TYPE = 'outlook'
GOOGLE_LINK_TYPE = 'google'
YAHOO_LINK_TYPE = 'yahoo'
ICAL_LINK_TYPE = 'ical'


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
        if link_type == ICAL_LINK_TYPE:
            response = HttpResponse(
                calendar_data['ical_content'],
                content_type=CALENDAR_CONTENT_TYPE)
            attachment = 'attachment; filename={title}.ics'.format(title=title)
            response['Content-Type'] = CALENDAR_CONTENT_TYPE
            response['Content-Disposition'] = attachment
        elif link_type == OUTLOOK_LINK_TYPE:
            response = HttpResponseRedirect(
                redirect_to=calendar_data['outlook_link'])
        elif link_type == GOOGLE_LINK_TYPE:
            response = HttpResponseRedirect(
                redirect_to=calendar_data['gcal_link'])
        elif link_type == YAHOO_LINK_TYPE:
            response = HttpResponseRedirect(
                redirect_to=calendar_data['yahoo_link'])
        else:
            response = JsonResponse(add2cal.as_dict())
        return response
