from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView
from blog.models import Post, Page

posts = list(range(1000))

PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    ordering = '-pk',
    paginate_by = PER_PAGE
    context_object_name = 'posts'
    queryset = Post.objects.get_published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': "Home - ",
        })
        return context
    

# def index(request):
#     posts = Post.objects.get_published()
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': "Home - ",
#         }
#     )


def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if page_obj is None:
        raise Http404()

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': f'Page - {page_obj.title} - ',
        }
    )


def post(request, slug):
    post_obj = Post.objects.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': f'Post - {post_obj.title} - ',
        }
    )
    
    
class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context = {}
        
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        user = User.objects.filter(id=id).first()
        
        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'user': user,
            'id': id,
        })
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        
        if user.first_name and user.last_name:
            user_full_name = f'{user.first_name} {user.last_name}'
            
        page_title = 'Author - ' + user_full_name + ' - '
        
        context.update({
            'page_title': page_title,
        })
        
        return context
    
    def get_queryset(self):
        self.queryset = super().get_queryset()
        self.queryset = self.queryset.filter(created_by__pk=self._temp_context['id'])
        return self.queryset
    

# def created_by(request, id):
#     user = User.objects.filter(pk=id).first()
    
#     if user is None:
#         raise Http404()
    
#     posts = Post.objects.get_published().filter(created_by__pk=id)
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     user_full_name = user.username
    
#     if user.first_name and user.last_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
        
#     page_title = 'Author - ' + user_full_name + ' - '
        

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )
    

class CategoryListView(PostListView):
    allow_empty = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page_title = f'Category - {self.get_queryset()[0].category.name} - '
        
        context.update({
            'page_title': page_title,
        })
        
        return context
        
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
    

# def category(request, slug):
#     if not slug:
#         return reverse('blog:index')

#     posts = Post.objects.get_published().filter(category__slug=slug)
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     if len(posts) == 0:
#         raise Http404()
    
#     page_title = f'Category - {posts[0].category.name} - '
    
#     return render(
#         request, 
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )
    
    
def tag(request, slug):
    if not slug:
        return reverse('blog:index')

    posts = Post.objects.get_published().filter(tags__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(posts) == 0:
        raise Http404()
    
    post_tag = posts[0].tags.filter(slug=slug).first()
    
    page_title = f'Tag - {post_tag.name} - '
    
    return render(
        request, 
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )
    

def search(request):
    search_value = request.GET.get('search', '').strip()
    
    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value)
    )[:PER_PAGE]
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': f'Search - {search_value[:30]} - ',
        }
    )