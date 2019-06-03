from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from add2cal import Add2Cal
import datetime
from rest_framework import renderers
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
    TemplateHTMLRenderer)

DATE_FORMAT = "%Y%m%dT%H%M%SZ"


class ICalRenderer(renderers.BaseRenderer):
    media_type = 'text/calendar'
    format = 'ics'

    def render(
            self,
            data,
            accepted_media_type=None,
            media_type=None,
            renderer_context=None):
        return data


class CalendarReminderView(APIView):
    view_name = 'calendar_reminder_view'

    permission_classes = (
        permissions.IsAuthenticated,
    )

    actions = ["GET"]

    renderer_classes = (
        ICalRenderer, BrowsableAPIRenderer,
        JSONRenderer, TemplateHTMLRenderer,)

    def get(self, request, format=None):
        params = self.request.query_params
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
            response = Response(
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
            return Response(add2cal.as_dict())
