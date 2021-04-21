from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    page = "home"
    context = {'setting':setting, 'page': page}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)

def contactus(request):
    if request.method == 'POST':# check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()# create relation with model
            data.name = form.cleaned_data['name']# get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()# save data to table
            messages.success(request, "Ваше сообщение отправлено. Спасибо.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form}
    return render(request, 'contactus.html', context)