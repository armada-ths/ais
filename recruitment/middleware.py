from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.http import urlquote
from django.core.urlresolvers import reverse


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
        # TODO: not hardcode fairs/2017/banquet/signup and fairs/2018/banquet/signup
        url_exceptions = {
            '/',
            '/api/events/', '/api/exhibitors/', '/api/news/', '/api/partners/',
            '/api/organization/', '/api/banquet_placement/', '/api/status/',
            '/register/', '/register/signup', '/register/new_company',
            '/register/password_reset/', '/register/password_reset/done/',
            '/register/external/signup',
            '/fairs/2017/banquet/signup', '/fairs/2018/banquet/signup'
        }

        # Since reset tokens are unique a startswith is necessary, this should later be implemented in settings.py with LOGIN_EXEMPT_URLS to avoid the logout part in the reset URL
        url_prefix_exceptions = {
            '/api/student_profile',
            '/register/reset/'
        }

        if path in url_exceptions:
            return
        for prefix in url_prefix_exceptions:
            if path.startswith(prefix, 0, len(prefix)):
                return
        if 'login' in path:
            return
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/?next=%s" % (urlquote(request.get_full_path())))
