import datetime
from haystack.indexes import *
from content.models import ContentRequest

class ContentRequestIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True, stored=False)

    ip_address = CharField(model_attr='ip_address')
    username = CharField(model_attr='username')

    url = CharField(model_attr='url')
    title = CharField(model_attr='fetch_title')
    
    domains = MultiValueField(model_attr='fetch_domains')
    
    referrer_domains = MultiValueField(model_attr='fetch_referrer_domains')

    referrer_url = CharField(model_attr='referrer_url', null=True)
    
    http_status = CharField(model_attr='http_status')

    content_type = CharField(model_attr='content_type')
    content_size = IntegerField(model_attr='content_size')
    content_path = CharField(model_attr='content_path')
    content_key = CharField(model_attr='content_key')
    
    retrieved = DateTimeField(model_attr='retrieved')
    
    search_terms = MultiValueField(model_attr='fetch_search_terms')
    
    parent_score = FloatField(model_attr='parent_score')

    content_url = CharField(model_attr='content_url')
    content_txt_url = CharField(model_attr='content_txt_url')

    def index_queryset(self, using=None):
        return ContentRequest.objects.all()

    def get_model(self):
        return ContentRequest

# site.register(ContentRequest, ContentRequestIndex)

