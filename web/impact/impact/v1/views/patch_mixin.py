from rest_framework.response import Response
from impact.v1.views.utils import valid_keys_note

REQUIRED_KEY_ERROR = "'{}' is required"
INVALID_KEY_ERROR = "'{}' is not a valid key."
NO_OBJECT_ERROR = "Unable to find object for id {}"


class PatchMixin(object):
    def patch(self, request, pk):
        object = self.helper_class.model.objects.filter(pk=pk).first()
        if not object:
            return Response(status=404, data=NO_OBJECT_ERROR.format(pk))
        helper = self.helper_class(object)
        keys = set(request.data.keys())
        self._invalid_keys(keys)
        valid_data = self.validate_keys(keys, request.data, helper)
        if helper.errors:
            return self.error_response(keys, helper)
        self.set_fields(valid_data, helper)
        return Response(status=204)

    def error_response(self, keys, helper):
        note = valid_keys_note(keys.intersection(
            set(self.helper_class.INPUT_KEYS)))
        return Response(status=403, data=helper.errors + [note])

    def set_fields(self, data, helper):
        for key, value in data.items():
            helper.field_setter(key, value)
        helper.save()

    def validate_keys(self, keys, data, helper):
        result = {}
        for key in keys.intersection(self.helper_class.INPUT_KEYS):
            result[key] = helper.validate(key, data[key])
        return result

    def _invalid_keys(self, keys):
        for key in set(keys) - set(self.helper_class.INPUT_KEYS):
            self.errors.append(INVALID_KEY_ERROR.format(key))
