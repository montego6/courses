import time
import logging

logger = logging.getLogger('api')

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        delta = time.time() - start
        if 'api' in request.path:
            self.log(request, response, delta)
        return response

    def log(self, request, response, delta):
        user = 'anonymous' if not request.user.is_authenticated else request.user.id
        logger.info('API call from user=%s method=%s uri=%s time=%s params=%s data=%s response=%s' % (
            user, request.method, request.path, delta, request.query_params, request.data, response.data
        ))
