import time

from apps.common.log_json import access_logger


class LogRequest:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        exec_time = int(time.time() - start_time)
        extra = {
            'url': request.get_full_path(),
            'exec_time': exec_time,
            'status_code': response.status_code,
            'method': request.method,
            'remote_addr': request.META.get('REMOTE_ADDR', '-'),
            'content_length': request.META.get('CONTENT_LENGTH', '-'),
            'user_agent': request.META.get('HTTP_USER_AGENT', '-'),
            'uid': request.user.id,
        }
        access_logger.info(msg='', extra=extra)
        return response
