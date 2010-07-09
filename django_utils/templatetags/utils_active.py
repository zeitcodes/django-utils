from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.tag(name="active_by_name")
def do_active_by_name(parser, token):
    try:
        tag_name = token.split_contents()[0]
        request = token.split_contents()[1]
        url_name = token.split_contents()[2]
        args = token.split_contents()[3:]
    except IndexError:
        raise template.TemplateSyntaxError, "%r requires at least 2 arguments." % tag_name
    return ActiveByName(request, url_name, args)

class ActiveByName(template.Node):
    def __init__(self, request, url_name, args):
        self.request = template.Variable(request)
        self.url_name = url_name
        self.args = [template.Variable(arg) for arg in args]

    def render(self, context):
        try:
            resolved_request = self.request.resolve(context)
            resolved_args = [str(arg.resolve(context)) for arg in self.args]
            url = reverse(self.url_name, args=resolved_args)
            pattern = '^' + url;
            import re
            if re.search(pattern, resolved_request.path):
                return 'active'
            return ''
        except template.VariableDoesNotExist:
            return ''
