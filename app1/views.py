# encoding:utf8
from django.contrib.auth.hashers import make_password
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render
from django.template import RequestContext
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from models import Image, User, Tag
from forms import ImgForm, RegisterForm, LoginForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required


def global_setting(request):
    cloud_list = Tag.objects.all()[:12]
    return {
        'cloud_list': cloud_list
    }


@login_required
def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render_to_response('publish_success.html', locals())
    else:
        form = ImgForm()
    return render_to_response('publish.html', locals())


def index(request):
    all_photos = Image.objects.all()
    photos = paging(request, all_photos)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


def detail(request):
    img = request.GET.get('img', None)
    photo = Image.objects.filter(img=img)
    return render_to_response('detail.html', locals())


def about(request):
    return render_to_response('about.html')


def contact(request):
    return render_to_response('contact.html')


# 分页
def paging(request, photos):
    paginator = Paginator(photos, 10)
    try:
        page = int(request.GET.get('page', 1))
        photos = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        photos = paginator.page(1)
    return photos


def do_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password']),
                email=form.cleaned_data['email'],
                mobile=form.cleaned_data['mobile']
            )
            user.save()
            return render(request, 'register_success.html')
    else:
        form = RegisterForm()
        return render_to_response('register.html', locals())


def do_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(index)
            else:
                return redirect(do_login)
    else:
        form = LoginForm()
        return render_to_response('login.html', locals())


def do_logout(request):
    logout(request)
    return redirect(index)
