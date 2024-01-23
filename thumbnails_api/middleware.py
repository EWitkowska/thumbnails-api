from django.conf import settings


class InternalIPsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        remote_addr = request.META.get("REMOTE_ADDR")
        if remote_addr and remote_addr not in settings.INTERNAL_IPS:
            settings.INTERNAL_IPS.append(remote_addr)

        return self.get_response(request)
