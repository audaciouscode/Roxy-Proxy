from django import forms
from django.utils.translation import ugettext as _

from models import LANGUAGES

SESSION_DURATIONS = (
    (30, _('30 minutes')),
    (60, _('1 hour')),
    (120, _('2 hours')),
    (240, _('4 hours')),
    (480, _('8 hours')),
    (1440, _('1 day')),
)

class ProfileForm(forms.Form):
    email = forms.EmailField(label=_('E-Mail Address'))
    first_name = forms.CharField(max_length=128, label=_('First Name'))
    last_name = forms.CharField(max_length=128, label=_('Last Name'))

    session_duration = forms.ChoiceField(choices=SESSION_DURATIONS, label=_('Session Duration'))
