from rest_framework.response import Response

from impact.v1.helpers import valid_keys_note

class PostMixin(object):
    def __init__(self):
        self.actions.append("POST")

    def post(self, request):
        object = self.create_object(request.POST)
        if self.errors:
            return Response(status=403, data=self.errors)
        
        return Response({"id": object.id})

    def create_object(self, post):
        raise NotImplementedError
