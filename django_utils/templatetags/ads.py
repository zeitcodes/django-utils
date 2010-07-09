from django import template
from collections import deque
from django.conf import settings


register = template.Library()


SERVICE_IDENTIFIER = getattr(settings, 'AD_SERVICE_IDENTIFIER', '')


ad_slots = deque()


@register.simple_tag
def register_ad(ad_unit):
    ad_slots.append(ad_unit)
    return "<!-- registered %s -->\n" % ad_unit


@register.simple_tag
def ad_header():
    ret = """
    <script type='text/javascript' src='http://partner.googleadservices.com/gampad/google_service.js'></script>
    <script type='text/javascript'>
        GS_googleAddAdSenseService("%s");
        GS_googleEnableAllServices();
    </script>
    <script type='text/javascript'>\n""" % SERVICE_IDENTIFIER
    while ad_slots:
        ad_slot = ad_slots.popleft()
        ret += 'GA_googleAddSlot("%s", "%s");\n' % (SERVICE_IDENTIFIER, ad_slot)
    ret += """
    </script>
    <script type='text/javascript'>
        GA_googleFetchAds();
    </script>"""
    return ret


@register.simple_tag
def ad_tag(ad_unit):
    return """
    <!-- %(identifier)s/%(ad_unit)s -->
    <script type='text/javascript'>
    GA_googleFillSlot("%(ad_unit)s");
    </script>""" % {'identifier': SERVICE_IDENTIFIER,
                    'ad_unit': ad_unit}