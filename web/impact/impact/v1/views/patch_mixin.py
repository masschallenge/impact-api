from rest_framework.response import Response
from .utils import valid_keys_note

NO_OBJECT_ERROR = "Unable to find object for id {}"


class PatchMixin(object):
    def patch(self, request, pk):
        object = self.helper_class.model.objects.filter(pk=pk).first()
        if not object:
            return Response(status=404, data=NO_OBJECT_ERROR.format(pk))
        helper = self.helper_class(object)
        keys = set(request.data.keys())
        self.invalid_keys(keys)
        valid_data = self.validate_keys(keys, request.data, helper)
        if self.errors:
            return self.error_response(keys)
        self.set_fields(valid_data, helper)
        return Response(status=204)

    def error_response(self, keys):
        note = valid_keys_note(self.helper_class.INPUT_KEYS)
        return Response(status=403, data=self.errors + [note])

    def set_fields(self, data, helper):
        for key, value in data.items():
            helper.field_setter(key, value)
        helper.save()

    def validate_keys(self, keys, data, helper):
        result = {}
        for key in keys.intersection(self.helper_class.INPUT_KEYS):
            result[key] = helper.validate(key, data[key])
        return result
