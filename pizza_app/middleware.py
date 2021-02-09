from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class IPFilterMiddleware:   

   def __init__(self, get_response):
      self.get_response = get_response

   def __call__(self, request):
      allowed_ip_addresses = settings.IPFILTER_MIDDLEWARE['ALLOWED_IP_ADDRESSES']
      client_ip_address = request.META.get('REMOTE_ADDR')

      if not client_ip_address in allowed_ip_addresses:
            raise PermissionDenied

      response = self.get_response(request)

      response['X-IP-FILTER'] = 'IP FILTER BY PIZZA SHOP'

      return response

#Unused until in production
class SSLifyMiddleware(object):
    """Force all requests to use HTTPs. If we get an HTTP request, we'll just
    force a redirect to HTTPs."""

    def process_request(self, request):
        secure_url = url.replace('http://', 'https://')
        return HttpResponsePermanentRedirect(secure_url)


