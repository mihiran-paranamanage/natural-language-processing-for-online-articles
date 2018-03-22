from django.urls import path
from . import views

app_name = 'cse_app'
urlpatterns = [
    # url : cse/
    path('', views.index, name='index'),
    # url : cse/sectors/7
    path('sectors/<int:val>', views.sectors, name='sectors'),
    # url : cse/news/256
    path('news/<int:comp_id>', views.news, name='news'),
    # url : cse/news/categories/256/award
    path('news/categories/<int:comp_id>/<str:val>', views.categories, name='categories'),
]
