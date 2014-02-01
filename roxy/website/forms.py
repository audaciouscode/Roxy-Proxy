import re

from django import forms

from models import *

# Via http://stackoverflow.com/questions/2532053/validate-hostname-string-in-python

def is_valid_domain(domainname):
    if len(domainname) > 255:
        return False
        
    if domainname[-1:] == ".":
        domainname = domainname[:-1]

    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    
    if len(domainname.split(".")) > 1:
        return all(allowed.match(x) for x in domainname.split("."))
        
    return False


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage


class BlacklistDomainForm(forms.Form):
    def clean_domain(self):
        data = self.cleaned_data['domain']
        
        if is_valid_domain(data) == False:
            raise forms.ValidationError("Please enter a valid domain name.")
        
        return data

    domain = forms.CharField(label='Blacklisted Domain')

