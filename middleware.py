import logging
logger = logging.getLogger('app')

class RequestLoggingMiddleware:
    def process_request(self, request):
        logger.debug(request)
        logger.debug('Logged Request')
        return None
