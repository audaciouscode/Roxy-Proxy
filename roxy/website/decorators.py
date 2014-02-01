from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def show_setup(function):
    def wrap(request, *args, **kwargs):
        profile = request.user.profile

        if profile.setup_shown:
            return function(request, *args, **kwargs)
        else:
            profile.setup_shown = True
            profile.save()
            
            return HttpResponseRedirect(reverse('setup'))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
