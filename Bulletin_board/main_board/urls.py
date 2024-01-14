from django.urls import path, re_path, register_converter
from django.views.decorators.cache import cache_page

from .views import *
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', BulletinHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BulletinCategory.as_view(), name='category'),
    path('message/', write_massage, name='message')

    # path('cats/<slug:cat_slug>/', categories_by_slug, name='cats_slug'),
    # path('archive/<year4:year>/', archive),

]