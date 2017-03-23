# encoding:utf8
from django.contrib.auth.hashers import make_password
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from models import Image, User, Tag, Comment
from forms import ImgForm, RegisterForm, LoginForm, CommentForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required


def global_setting(request):
    cloud_list = Tag.objects.all()[:12]
    hit_list = Image.objects.all().order_by('-likes')[:6]
    latest_list = Image.objects.all().order_by('-publish_date')[:6]
    return {
        'cloud_list': cloud_list,
        'hit_list': hit_list,
        'latest_list': latest_list,
    }


@login_required
def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image.objects.create(
                name=form.cleaned_data['img_url'],
                img_url=form.cleaned_data['img_url'],
                desc=form.cleaned_data['desc'],
                user=request.user
            )
            try:
                form.save()
            except:
                pass
            return render(request, 'publish_success.html', locals())
    else:
        form = ImgForm()
    return render(request, 'publish.html', locals())


def index(request):
    all_photos = Image.objects.all()
    photos = paging(request, all_photos)
    return render(request, 'index.html', locals())


def detail(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                comment_text=form.cleaned_data['comment_text'],
                user=request.user,
                img=Image(str(request.META['HTTP_REFERER']).split('=')[1])
            )
            comment.save()
            return redirect(request.META['HTTP_REFERER'])

    else:
        form = Comment()
        id = request.GET.get('id', None)
        photos = Image.objects.filter(id=id)
        comments = Comment.objects.filter(img=id)
        return render(request, 'detail.html', locals())


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# 分页
def paging(request, photos):
    paginator = Paginator(photos, 8)
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
            errors = "注册信息有误,请确认"
            return render(request, 'register.html', locals())
    else:
        form = RegisterForm()
        return render(request, 'register.html', locals())


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
            errors = '用户名或密码错误'
            return render(request, 'login.html', locals())
    else:
        form = LoginForm()
        return render(request, 'login.html', locals())


def do_logout(request):
    logout(request)
    return redirect(index)


def list(request):
    tag = request.GET.get('tag', None)
    tag_id = Tag.objects.values('id').filter(name=tag)
    images = Image.objects.filter(tag=tag_id)
    photos = paging(request, images)
    return render(request, 'index.html', locals())
