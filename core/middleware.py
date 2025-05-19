import time
from django.conf import settings
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.urls import reverse

class AbsoluteSessionTimeoutMiddleware:
    """
    Forces logout after a fixed time (SESSION_COOKIE_AGE, e.g. 3 hours) from login, regardless of activity.
    Add 'core.middleware.AbsoluteSessionTimeoutMiddleware' to MIDDLEWARE after AuthenticationMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = int(time.time())
            session_start = request.session.get('session_start')
            max_age = getattr(settings, 'SESSION_COOKIE_AGE', 10800)
            if not session_start:
                request.session['session_start'] = now
            elif now - session_start > max_age:
                auth.logout(request)
                messages.info(request, 'Session expired: You have been logged out after 3 hours.')
                return redirect(reverse('login'))
        response = self.get_response(request)
        return response
