from rest_framework.response import Response
from impact.v1.views.utils import valid_keys_note

REQUIRED_KEY_ERROR = "'{}' is required"


class PostMixin(object):
    def post(self, request):
        object = self.create_object(request.POST)
        if self.errors:
            return Response(status=403, data=self.errors)
        return Response({"id": object.id})

    def create_object(self, post_data):
        object_data = self.data_from_post(post_data)
        self.invalid_keys(post_data.keys())
        if self.errors:
            note = valid_keys_note(self.helper_class.ALL_KEYS)
            self.errors.append(note)
            return None
        return self.helper_class.construct_object(object_data)

    def data_from_post(self, post_data):
        self.check_required_keys(post_data)
        results = self.copy_keys(post_data, self.helper_class.ALL_KEYS)
        self._validate_args(results, self.helper_class.VALIDATORS)
        return results

    def check_required_keys(self, posted_data, required_keys=None):
        keys = required_keys or self.helper_class.REQUIRED_KEYS
        for key in set(keys) - set(posted_data):
            self.errors.append(REQUIRED_KEY_ERROR.format(key))

    def copy_keys(self, data, keys):
        result = {}
        for key in keys:
            if key in data:
                result[key] = data[key]
        return result

    def _validate_args(self, args, validators):
        for key, validator in validators.items():
            if key in args:
                if validator:
                    args[key] = validator(self, key, args[key])
