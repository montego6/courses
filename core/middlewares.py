import time
import logging
import copy

from core.helpers import get_client_ip

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
        response_body = response.content if hasattr(response, 'data') else None
        ip = get_client_ip(request)
        logger.info('API call from ip=%s user=%s method=%s uri=%s time=%s params=%s response=%s' % (
            ip, user, request.method, request.path, 
            delta, request.META['QUERY_STRING'],  
            response_body
        ))
