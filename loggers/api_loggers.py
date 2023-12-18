import logging
from rest_framework.views import APIView

logger = logging.getLogger('api')


class APIFullResponseLogger(APIView):
    def finalize_response(self, request, response, *args, **kwargs):
        user = 'anonymous' if not request.user.is_authenticated else request.user.id
        logger.info('API call from user=%s method=%s uri=%s params=%s data=%s response=%s' % (
            user, request.method, request.path, request.query_params, request.data, response.data
        ))
        return super().finalize_response(request, response, *args, **kwargs)
    

