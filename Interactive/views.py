from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.mail import send_mail

from Interactive.forms import ContactForm, CustomerForm
from Interactive.models import Customer
from Interactive.forms import AddNewAddressDeliveryForm, Delivery
from Shop.models import Cart


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


class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Customer
    success_url = reverse_lazy('profile')
    template_name = 'pages/profile.html'
    form_class = CustomerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        form_class = CustomerForm(instance=customer)
        context['form'] = form_class
        return context

    def post(self, request, *args, **kwargs):
        customer = self.request.user.customer
        form = CustomerForm(self.request.POST, self.request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('profile'), permanent=True)


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


class DeliveryFormView(LoginRequiredMixin, FormView):
    template_name = 'pages/delivery.html'
    form_class = AddNewAddressDeliveryForm
    success_url = '/delivery/'
    # Вместо 404 и перенаправления, пометка, доступ запрещен
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = \
            Delivery.objects.filter(user=self.request.user.id).values('id', 'user_id', 'address_header')

        context['cart_items'] = Cart.objects.filter(user=self.request.user.id).select_related('product')
        return context

    def form_valid(self, form):
        form.save()
        print(form.cleaned_data)
        return super(DeliveryFormView, self).form_valid(form)

