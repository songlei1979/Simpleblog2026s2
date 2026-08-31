from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import PostCreateForm
from blog.models import Category, Post


# Create your views here.
def home(request):
    return render(request, 'blog/home.html')


def categories(request):
    categories = Category.objects.all()
    return render(request,
                  'blog/categories.html',
                  {'categories': categories})


def posts(request):
    posts = Post.objects.all()
    users = User.objects.all()
    categories = Category.objects.all()
    return render(request,
                  'blog/posts.html',
                  {
                      'posts': posts,
                      'users': users,
                      'categories': categories
                  })


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, "blog/category_detail.html",
                  {'category': category})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "blog/post_detail.html",
                  {'post': post})


def category_create(request):
    category_name = request.POST['name']
    category = Category.objects.create(name=category_name)
    return redirect('categories')


def category_update(request, category_id):
    category = Category.objects.get(id=category_id)
    category.name = request.POST['name']
    category.save()
    return redirect('categories')


def category_delete(request):
    category_id = request.POST['category_id']
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('categories')


def post_create(request):
    title = request.POST['title']
    header_image = request.FILES['header_image']
    title_tag = request.POST['title_tag']
    author = User.objects.get(id=request.POST['author'])
    body = request.POST['body']
    snippet = request.POST['snippet']
    category = Category.objects.get(id=request.POST['category'])

    post = Post.objects.create(title=title,
                               header_image=header_image,
                               title_tag=title_tag,
                               author=author,
                               body=body,
                               snippet=snippet,
                               category=category)
    return redirect('posts')


class PostList(TemplateView):
    template_name = "blog/posts_template_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        print(context)
        print(type(context))
        return context

class PostList_Generic(ListView):
    model = Post
    template_name = "blog/posts_list_view.html"

class PostDetail_Generic(DetailView):
    model = Post
    template_name = "blog/post_detail_view.html"

class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_create_view.html"
    success_url = "/post_list_view"
    form_class = PostCreateForm


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_update_view.html"
    success_url = "/post_list_view"
    form_class = PostCreateForm

class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_delete_view.html"
    success_url = "/post_list_view"



