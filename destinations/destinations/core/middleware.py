from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from .models import Session

# Paths that should be publicly accessible without authentication
ALLOWED_PATH_PREFIXES = (
    '/static/',
    '/users/new',    # signup form
    '/users',        # signup POST
    '/sessions/new', # login form
    '/sessions',     # login POST
    '/admin/',
    '/',             # index/home
)


def login_exempt(view_func):
    setattr(view_func, 'login_exempt', True)
    return view_func


class SessionLookupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('session_token')
        request.current_session = None
        request.current_user = None

        if token:
            session = Session.objects.filter(token=token).select_related('user').first()
            if session:
                request.current_session = session
                request.current_user = session.user

        return self.get_response(request)


class AuthEnforcementMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # If user is already authenticated, allow
        if getattr(request, 'current_session', None):
            return None

        # Allow explicit view-level exemptions
        if getattr(view_func, 'login_exempt', False):
            return None

        # Allow allowed path prefixes
        path = request.path
        for prefix in ALLOWED_PATH_PREFIXES:
            if path == prefix or path.startswith(prefix):
                return None

        # Not authenticated, not exempt -> redirect to login form
        return redirect('/sessions/new/')