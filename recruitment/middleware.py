from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.http import urlquote



class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        # PLACEHOLDER until proper authenitaction is in place
        path = request.path_info
        if path == '/api/events/' or \
                path == '/api/news/' or \
                path == '/api/exhibitors/':
            return
        if not request.user.is_authenticated():
            if path != '/' and not 'login' in path:
                return HttpResponseRedirect("/?next=%s" % (urlquote(request.get_full_path())))
