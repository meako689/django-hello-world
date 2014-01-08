from models import RecordedRequest

class RequestRecordMiddleware(object):
    def process_request(self, request):
        """Record each request"""
        RecordedRequest.from_request(request)
