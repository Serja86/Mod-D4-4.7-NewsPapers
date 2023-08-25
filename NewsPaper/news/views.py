from django.shortcuts import render
from django.urls import reverse_lazy


# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import PostSearch
from .forms import PostForm

class NewsList(ListView):
   model = Post
   ordering = 'title'
   template_name = 'News.html'
   context_object_name = 'news'
   extra_context = {'title': 'Новости'}
   author = 'author'
   # queryset = Post.objects.order_by('-dateCreation')
   paginate_by = 10

   # Переопределяем функцию получения списка товаров
   def __init__(self, **kwargs):
       super().__init__(kwargs)
       self.filterset = None

   def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostSearch(self.request.GET, queryset)
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       return context

   def post_search(request):
       f = PostSearch(request.GET,
                      queryset=Post.objects.all())
       return render(request,
                     'news_search.html',
                     {'filter': f})


class NewsDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'

class PostSearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'NewsSearch'
    paginate_by = 10
    ordering = ['-id']
    queryset = Post.objects.all()

    def get_filter(self):
        return PostSearch(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'filter': self.get_filter(),
        }

class PostCreateAR(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = "AR"
        return super().form_valid(form)

class PostCreateNW(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = "NW"
        return super().form_valid(form)



class PostEditNW(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class PostDeleteNW(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class PostEditAR(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

class PostDeleteAR(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')
