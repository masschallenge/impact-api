import traceback

from django.conf import settings
from graphene_django.views import GraphQLView
from graphql.error import GraphQLSyntaxError
from graphql.error.located_error import GraphQLLocatedError
from graphql.error import format_error as format_graphql_error
from impact.graphql.utils.response_error import ResponseError
from impact.graphql.utils.str_converters import to_kebab_case, dict_key_to_camel_case


def encode_code(code):
    if code is None:
        return None
    return to_kebab_case(code)


def encode_params(params):
    if params is None:
        return None
    return dict_key_to_camel_case(params)


def format_response_error(error: ResponseError):
    return {
        'message': error.message,
        'code': encode_code(error.code),
        'params': encode_params(error.params),
    }


def format_internal_error(error: Exception):
    message = 'Internal server errorr'
    code = 'internal-server-error'
    if settings.DEBUG:
        params = {
            'exception': type(error).__name__,
            'message': str(error),
            'trace': traceback.format_list(traceback.extract_tb(error.__traceback__)),
        }
        return {
            'code': code,
            'message': message,
            'params': params,
        }
    return {
        'code': code,
        'message': message,
    }


def format_located_error(error):
    if isinstance(error.original_error, GraphQLLocatedError):
        return format_located_error(error.original_error)
    if isinstance(error.original_error, ResponseError):
        return format_response_error(error.original_error)
    return format_internal_error(error.original_error)


class SafeGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        try:
            if isinstance(error, GraphQLLocatedError):
                return format_located_error(error)
            if isinstance(error, GraphQLSyntaxError):
                return format_graphql_error(error)
        except Exception as e:
            return format_response_error(e)
