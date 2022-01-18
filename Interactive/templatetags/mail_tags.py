from django import template

from Interactive.forms import MailForm

register = template.Library()


@register.inclusion_tag('templatetags/mail.html')
def mail_form():
    return {'mail_form': MailForm()}
