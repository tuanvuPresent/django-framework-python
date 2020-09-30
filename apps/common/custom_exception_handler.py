from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    exc_class = exc.__class__.__name__
    if response is not None:
        if exc_class == 'ValidationError':
            detail = response.data
            messenger = get_full_errors_messages(detail)

            errors = get_errors_code(detail)
            print(errors)

        else:
            messenger = response.data.get('detail')

        error_code = response.status_code
        status_code = response.status_code
    else:
        error_code = 500
        messenger = str(exc)
        status_code = 500

    return Response({
        'status': False,
        'errorCode': error_code,
        'messenger': messenger
    }, status=status_code)


def get_errors_code(detail):
    if isinstance(detail, list):
        for item in detail:
            if item:
                return get_errors_code(item)
    elif isinstance(detail, dict):
        for key, value in detail.items():
            return '{}_{}'.format(key, get_errors_code(value))
    elif isinstance(detail, ErrorDetail):
        return detail.code


def get_full_errors(detail):
    if isinstance(detail, list):
        errors = [get_full_errors(item) for item in detail if item]
        if len(errors) > 1:
            return errors
        return errors[0]
    elif isinstance(detail, dict):
        return {key: get_full_errors(value) for key, value in detail.items()}
    return {
        'message': detail,
        'code': detail.code
    }


def get_full_errors_codes(detail):
    if isinstance(detail, list):
        errors = [get_full_errors_codes(item) for item in detail if item]
        if len(errors) > 1:
            return errors
        return errors[0]
    elif isinstance(detail, dict):
        return {key: get_full_errors_codes(value) for key, value in detail.items()}
    return detail.code


def get_full_errors_messages(detail):
    if isinstance(detail, list):
        errors = [get_full_errors_messages(item) for item in detail if item]
        if len(errors) > 1:
            return errors
        return errors[0]
    elif isinstance(detail, dict):
        return {key: get_full_errors_messages(value) for key, value in detail.items()}
    return detail


class CustomAPIException(APIException):
    status_code = 400

    def __init__(self, messenger=None, code=None):
        self.code = code
        if code is not None and code > 300:
            self.status_code = code
        super().__init__(detail=messenger, code=code)
