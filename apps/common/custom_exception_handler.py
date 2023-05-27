import logging

from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler
from apps.common.custom_model_view_set import BaseResponse
from apps.common.constant import ErrorMessage
from sentry_sdk import capture_exception


def custom_exception_handler(exc, context):
    logger = logging.getLogger(str(context['view']))
    response = exception_handler(exc, context)
    if response is not None:
        status_code = response.status_code
        detail = None
        exc_class = exc.__class__.__name__
        if exc_class == 'ValidationError':
            error = ErrorMessage.UNKNOWN_ERROR
            detail = get_full_errors_messages(response.data)
        elif exc_class == "AuthenticationFailed":
            error = ErrorMessage.INVALID_AUTH
        elif exc_class == "CustomAPIException":
            error = exc.detail
        elif exc_class == "Http404":
            error = ErrorMessage.NOT_FOUND
        elif exc_class == "MethodNotAllowed":
            error = ErrorMessage.NOT_ALLOW_METHOD
        elif exc_class == "NotAuthenticated":
            error = ErrorMessage.NOT_AUTH
        elif exc_class == "PermissionDenied":
            error = ErrorMessage.NOT_PERMISSION
        elif exc_class == "Throttled":
            error = ErrorMessage.THROTTLED_REQUEST
        else:
            error = ErrorMessage.UNKNOWN_ERROR
            detail = str(exc)

    else:
        detail = str(exc)
        error = ErrorMessage.UNKNOWN_ERROR
        status_code = 500
        logger.error(exc)
        capture_exception(exc)
    return Response(BaseResponse(
        status=False,
        message=error.message,
        code=error.code,
        data=detail
    ).data, status=status_code)


def get_errors_code(detail):
    if isinstance(detail, list):
        for item in detail:
            if item:
                return get_errors_code(item)
    elif isinstance(detail, dict):
        for key, value in detail.items():
            return f'{key}_{get_errors_code(value)}'
    elif isinstance(detail, ErrorDetail):
        return detail.code
    

def get_messages(detail, prefix=""):
    errors = {}
    if isinstance(detail, list):
        for i, item in enumerate(detail):
            key = f"{prefix}[{i}]" if prefix else ''
            errors.update(get_messages(item, prefix=key))
    elif isinstance(detail, dict):
        for key, value in detail.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            errors.update(get_messages(value, prefix=new_prefix))
    else:
        if prefix[-1] == ']':
            prefix = prefix[:-3]
        errors[prefix] = detail

    return errors
    

def get_full_errors(detail):
    if isinstance(detail, list):
        errors = [get_full_errors(item) for item in detail if item]
        return errors if len(errors) > 1 else errors[0]
    elif isinstance(detail, dict):
        return {key: get_full_errors(value) for key, value in detail.items()}
    return {
        'message': detail,
        'code': detail.code
    }


def get_full_errors_codes(detail):
    if isinstance(detail, list):
        errors = [get_full_errors_codes(item) for item in detail if item]
        return errors if len(errors) > 1 else errors[0]
    elif isinstance(detail, dict):
        return {key: get_full_errors_codes(value) for key, value in detail.items()}
    return detail.code


def get_full_errors_messages(detail):
    if isinstance(detail, list):
        errors = [get_full_errors_messages(item) for item in detail if item]
        return errors if len(errors) > 1 else errors[0]
    elif isinstance(detail, dict):
        return {key: get_full_errors_messages(value) for key, value in detail.items()}
    return detail


class CustomAPIException(APIException):
    status_code = 400

    def __init__(self, message=None, code=None):
        self.code = code
        self.detail = message
