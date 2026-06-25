class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.brokerage = self.get_brokerage(request)
        return self.get_response(request)

    def get_brokerage(self, request):
        user = getattr(request, 'user', None)

        if not user or not user.is_authenticated:
            return None

        if user.is_superuser:
            return None

        return user.brokerage
