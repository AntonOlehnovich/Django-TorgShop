import csv
import datetime
import tempfile

import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from weasyprint import HTML

from TorgShop import settings
from home.models import FAQ
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile

@login_required(login_url='/login') # Check login
def index(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {#'category': category,
               'profile': profile}
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Ошибка авторизации! Имя или пароль некорректны")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.
    #category = Category.objects.all()
    context = { }
    return render(request, 'login_form.html', context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Ваш аккаунт успешно создан!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')
    form = SignUpForm()
    #category = Category.objects.all()
    context = {#'category': category,
               'form': form,}
    return render(request, 'signup_form.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return HttpResponseRedirect('/user')
    else:
        #category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            #'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Ваш пароль успешно изменён!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,  #'category': category
                                                      })


@login_required(login_url='/login') # Check login
def user_orders(request):
    #category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {#'category': category,
               'orders': orders, }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login') # Check login
def user_orderdetail(request, id):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login') # Check login
def user_orders_product(request):
    #category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id)
    context = {#'category': category,
               'order_product': order_product, }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/login') # Check login
def user_order_product_detail(request, id, oid):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    #category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        #'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Отзыв удалён')
    return HttpResponseRedirect('/user/comments')


def faq(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    if defaultlang == currentlang:
        faq = FAQ.objects.filter(status="True", lang=defaultlang).order_by("ordernumber")
    else:
        faq = FAQ.objects.filter(status="True", lang=currentlang).order_by("ordernumber")

    context = {
        'faq': faq,
    }
    return render(request, 'faq.html', context)

def export_csv(request, id):
    response = HttpResponse(content_type='text/csv; charset=windows-1251')
    response['Content-Disposition'] = 'attachment; filename= Orders' + \
        str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Список заказа'])
    writer.writerow(['Название продукта', 'Цена', 'Количество', 'Сумма', 'Статус', 'Дата'])
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    total = 0
    for rs in orderitems:
        total += rs.amount
        if rs.product.variant == 'None':
            writer.writerow([rs.product.title, 'Br '+str(rs.price), rs.quantity, rs.amount, rs.status, rs.create_at])
        else:
            writer.writerow(
                [rs.product.title + " " + str(rs.variant.size) + " " + str(rs.variant.color), 'Br ' + str(rs.price), rs.quantity, rs.amount,
                 rs.status, rs.create_at])
    writer.writerow([])
    writer.writerow(['Итого к оплате', 'Br '+str(total)])
    writer.writerow([])
    writer.writerow(['Детали заказа'])
    writer.writerow(['Имя Фамилия', 'Телефон', 'Адрес', 'Город', 'Страна', 'Статус', 'Дата'])
    writer.writerow([order.first_name + ' ' + order.last_name, order.phone, order.address, order.city, order.country, order.status,
                     order.create_at])
    return response


def export_excel(request, id):
    response = HttpResponse(content_type='application/ms-excel; charset=windows-1251')
    response['Content-Disposition'] = 'attachment; filename= Orders' + \
                                      str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet('Orders')
    row_num = 0
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    font_style = xlwt.XFStyle()
    font_style_1 = xlwt.XFStyle()
    font_style_2 = xlwt.XFStyle()
    font_style_3 = xlwt.easyxf('pattern: pattern solid, fore_colour violet;')
    font_style.alignment = alignment
    font_style_1.alignment = alignment
    font_style_2.alignment = alignment
    font_style.font.bold = True
    font_style_1.font.bold = False
    font_style.font.colour_index = xlwt.Style.colour_map['orange']
    font_style_1.font.colour_index = xlwt.Style.colour_map['blue']
    font_style_2.font.colour_index = xlwt.Style.colour_map['green']
    ws.write(row_num, 0, 'Список заказа', font_style_2)
    row_num += 1
    columns = ['Название продукта', 'Класс энергопотребления','Цвет',  'Цена', 'Количество', 'Сумма', 'Статус', 'Дата']
    columns_1 = ['Имя Фамилия', 'Телефон', 'Адрес', 'Город', 'Страна', 'Статус', 'Дата']
    ws.col(0).width = 256 * 40
    ws.col(1).width = 256 * 30
    ws.col(2).width = 256 * 30
    ws.col(3).width = 256 * 20
    ws.col(4).width = 256 * 20
    ws.col(5).width = 256 * 15
    ws.col(6).width = 256 * 30
    ws.col(7).width = 256 * 40
    ws.col(8).width = 256 * 40

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    columns_2 = [order.first_name + ' ' + order.last_name, order.phone, order.address, order.city,
                 order.country, order.status, order.create_at]
    orderitems = OrderProduct.objects.filter(order_id=id).values_list('product__title', 'variant__size__name', 'variant__color__name', 'price', 'quantity',
                                                                      'amount', 'status', 'create_at')
    orderitem = OrderProduct.objects.filter(order_id=id)
    total = 0
    for rs in orderitem:
        total += rs.amount
    for row in orderitems:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style_1)
    row_num += 1
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, '', font_style_3)
    row_num += 1
    ws.write(row_num, 0, 'Итого к оплате', font_style)
    ws.write(row_num, 1, 'Br ' + str(total), font_style_1)
    row_num += 1
    ws.write(row_num, 0, '', font_style_3)
    ws.write(row_num, 1, '', font_style_3)
    row_num += 1
    ws.write(row_num, 0, 'Детали заказа', font_style_2)
    row_num += 1
    for col_num in range(len(columns_1)):
        ws.write(row_num, col_num, columns_1[col_num], font_style)
    row_num += 1
    for col_num in range(len(columns_2)):
        ws.write(row_num, col_num, str(columns_2[col_num]), font_style_1)
    row_num += 1
    for col_num in range(len(columns_2)):
        ws.write(row_num, col_num, '', font_style_3)
    wb.save(response)
    return response


def export_pdf(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= Orders' + \
                                      str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    total = 0
    for rs in orderitems:
        total += rs.amount
    html_string = render_to_string(
        'pdf-output.html', {'orderitems': orderitems, 'order': order, 'total': total})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response