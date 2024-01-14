from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *


class BulletinHome(DataMixin, ListView):
	model = Bulletin
	template_name = 'main_board/index.html'
	context_object_name = 'posts'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Главная страница')
		return dict(list(context.items()) + list(c_def.items()))

	def get_queryset(self):
		return Bulletin.objects.filter(is_published=True)


# def index(request):
# 	posts = Bulletin.objects.all()
#
# 	context = {
# 		'posts': posts,
# 		'menu': menu,
# 		'title': 'Главная страница',
# 		'cat_selected': 0,
# 	}
# 	return render(request, 'main_board/index.html', context=context)


def about(request):
	return render(request, 'main_board/about.html', {'title': 'О сайте', 'menu': menu})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
	form_class = AddPostForm
	template_name = 'main_board/addpage.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('home')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Добавление объявления')
		return dict(list(context.items()) + list(c_def.items()))


# def add_page(request):
# 	if request.method == 'POST':
# 		form = AddPostForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			# print(form.cleaned_data)
# 			form.save()
# 			return redirect('home')
# 	else:
# 		form = AddPostForm()
# 	return render(request, 'main_board/addpage.html', {'form': form, 'title': 'Добавление объявления', 'menu': menu})


def contact(request):
	return render(request, 'main_board/contact.html', {'title': 'Контакты', 'menu': menu})


# def login(request):
# 	return render(request, 'main_board/login.html', {'title': 'Вход/Регистрация', 'menu': menu})


def write_massage(request):
	return render(request, 'main_board/message.html', {'title': 'Message', 'menu': menu})


class ShowPost(DataMixin, DetailView):
	model = Bulletin
	template_name = 'main_board/post.html'
	slug_url_kwarg = 'post_slug'
	context_object_name = 'post'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title=context['post'])
		return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
# 	post = get_object_or_404(Bulletin, slug=post_slug)
#
# 	context = {
# 		'post': post,
# 		'menu': menu,
# 		'title': post.title,
# 		'cat_selected': post.cat_id,
# 	}
# 	return render(request, 'main_board/post.html', context=context)


class BulletinCategory(DataMixin, ListView):
	model = Bulletin
	template_name = 'main_board/index.html'
	context_object_name = 'posts'
	allow_empty = False

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c = Category.objects.get(slug=self.kwargs['cat_slug'])
		c_def = self.get_user_context(title='Категория -' + str(c.name),
									  cat_selected=c.pk)
		return dict(list(context.items()) + list(c_def.items()))

	def get_queryset(self):
		return Bulletin.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# def show_category(request, cat_id):
# 	posts = Bulletin.objects.filter(cat_id=cat_id)
# 	cats = Category.objects.all()
# 	if len(posts) == 0:
# 		raise Http404()
#
# 	context = {
# 		'posts': posts,
# 		'menu': menu,
# 		'title': cats[cat_id-1],
# 		'cat_selected': cat_id,
# 	}
# 	return render(request, 'main_board/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
	form_class = RegisterUserForm
	template_name = 'main_board/register.html'
	success_url = reverse_lazy('login')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title="Регистрация")
		return dict(list(context.items()) + list(c_def.items()))

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')


class LoginUser(DataMixin, LoginView):
	form_class = LoginUserForm
	template_name = 'main_board/login.html'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title="Авторизация")
		return dict(list(context.items()) + list(c_def.items()))

	def get_success_url(self):
		return reverse_lazy('home')


def logout_user(request):
	logout(request)
	return redirect('home')


def page_not_found(request, exception):
	return HttpResponseNotFound("<h1>Страница не найдена</h1>")
