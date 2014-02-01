from django import forms

from models import SESSION_TYPE

SESSION_DURATION = (
    (30, '30 minutes'),
    (60, '1 hour'),
    (120, '2 hours'),
)

class SessionForm(forms.Form):
    session_type = forms.ChoiceField(choices=SESSION_TYPE)
    duration = forms.ChoiceField(choices=SESSION_DURATION)

