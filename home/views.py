from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage
from product.models import Category, Product


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]   #first 4 products
    products_latest = Product.objects.all().order_by('-id')[:4]  #last 4 products
    products_picked = Product.objects.all().order_by('?')[:4]    #random selected 4 products
    page = "home"
    context = {'setting': setting,
               'page': page,
               'products_slider': products_slider,
               'products_latest': products_latest,
               'products_picked': products_picked,
               'category': category}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()# временно
    context = {'setting': setting, 'category': category}
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
    category = Category.objects.all()# временно
    form = ContactForm
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'contactus.html', context)

def category_products(request, id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'catdata': catdata}
    return render(request, 'category_products.html', context)

def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query': query,
                       'category': category}
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')