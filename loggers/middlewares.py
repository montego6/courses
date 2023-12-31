import time
import logging

logger = logging.getLogger('api')

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        delta = (time.time() - start) * 1000
        if 'api' in request.path:
            self.log(request, response, delta)
        return response
    
    def process_exception(self, request, exception):
        logger.error('Exception %s for API call method=%s uri=%s params=%s data=%s' % (
            exception, request.method, request.path, request.META['QUERY_STRING'], request.body
        ))
        logger.error(exception, exc_info=True)
        return None

    def log(self, request, response, delta):
        user = 'anonymous' if not request.user.is_authenticated else request.user.id
        logger.info('API call from user=%s method=%s uri=%s time=%s params=%s data=%s response=%s' % (
            user, request.method, request.path, 
            delta, request.META['QUERY_STRING'], request.body, 
            response.data
        ))
