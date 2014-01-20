from django import forms
from haystack.forms import SearchForm

class RoxyContentSearchForm(SearchForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    domain = forms.CharField(required=False)
    title = forms.CharField(required=False)
    referrer = forms.CharField(required=False)
    content_type = forms.CharField(required=False)
    content_size = forms.IntegerField(required=False)
    parent_score = forms.FloatField(required=False)

    def search(self):
        sqs = super(RoxyContentSearchForm, self).search()
        
        try:
            if self.cleaned_data['start_date']:
                sqs = sqs.filter(retrieved__gte=self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                sqs = sqs.filter(retrieved__lte=self.cleaned_data['end_date'])

            if self.cleaned_data['content_type']:
                sqs = sqs.filter(content_type=self.cleaned_data['content_type'])

            if self.cleaned_data['content_size']:
                sqs = sqs.filter(content_size__gte=self.cleaned_data['content_size'])

            if self.cleaned_data['parent_score']:
                sqs = sqs.filter(parent_score__gte=self.cleaned_data['parent_score'])

            if self.cleaned_data['domain']:
                sqs = sqs.filter(domains=self.cleaned_data['domain'])

            if self.cleaned_data['referrer']:
                sqs = sqs.filter(referrer_domains=self.cleaned_data['referrer'])
                
            if self.cleaned_data['title']:
                sqs = sqs.filter(title=self.cleaned_data['title'])
            
        except AttributeError:
            pass
        
        return sqs
