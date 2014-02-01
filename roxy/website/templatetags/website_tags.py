from django import template
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

register = template.Library()

class HeaderMenuNode(template.Node):
    def __init__(self):
        self.request = template.Variable('request')

    def render(self, context):
        request = self.request.resolve(context)

        return render_to_string('', RequestContext(request))

@register.inclusion_tag('templatetags/header_menu.html', takes_context=True)
def header_menu(context):
    return {'request': context['request']}


class UseHeaderNode(template.Node):
    def __init__(self, template_path):
        self.template_path = template_path

    def render(self, context):
        return render_to_string(self.template_path, context)

@register.tag(name='use_header')
def use_header(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return UseHeaderNode(format_string[1:-1])


class UseFooterNode(template.Node):
    def __init__(self, template_path):
        self.template_path = template_path

    def render(self, context):
        return render_to_string(self.template_path, context)

@register.tag(name='use_footer')
def use_footer(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return UseFooterNode(format_string[1:-1])
