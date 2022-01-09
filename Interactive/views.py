from django.views.generic import FormView, CreateView
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from Interactive.forms import ContactForm
from django.conf import settings


def ex404(request, exception):
    context = {'errorMessage': 'We Couldn’t Find this Page'}
    print(exception)
    if isinstance(exception, int):
        context['errorMessage'] = 'Новость не существует'
    request = render(request, 'exception/404.html', status=404, context=context)
    return request


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ContactFormView(FormView):
    template_name = 'pages/contact-us.html'
    form_class = ContactForm
    success_url = '/contact/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CONTACT US'
        context['contact_selected'] = 'active'
        contact_info = (
            'E-Shopper Inc.',
            '935 W. Webster Ave New Streets Chicago, IL 60614, NY',
            'New York USA',
            'Mobile: +2346 17 38 93',
            'Fax: 1-714-252-0026',
            'Email: info@e-shopper.com',
        )
        context['contact_info'] = contact_info

        context['headline'] = (
            'Contact US', 'get in touch', 'contact info', 'SOCIAL NETWORKING'
        )
        context['social_networking'] = (
            ('fa-facebook', '#'),
            ('fa-twitter', '#'),
            ('fa-google-plus', '#'),
            ('fa-youtube', '#')
        )
        return context

    def form_valid(self, form):
        form = form.cleaned_data
        print(form)
        send_mail(form['name'],
                  ('Отправитель: {} \nТекст сообщеня:\n{}').format(form['email'], form['text']),
                  settings.EMAIL_HOST_USER,
                  [settings.EMAIL_HOST_USER],
                  fail_silently=False)

        return super(ContactFormView, self).form_valid(form)


