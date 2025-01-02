from django.shortcuts import get_object_or_404,render
from .models import Post
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django .views.generic import ListView
# Create your views here.


def post_list(request):
    post_list = Post.published.all()
    #doing a paginator with only 4 post per list
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        # if page is not an integer get first page in its place, also # if the page number is out of range get lastpage result
        posts = paginator.page(1 if isinstance(page_number, int) else paginator.num_pages)


    return render(
        request,
        'spotlightcentral/post/list.html',
    {'posts': posts}
    )


def post_details(request, year, month, day, slug):
    # try:
    #     post = Post.published.get(id = id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post Found.")

    post = get_object_or_404(
        Post,  # Corrected model name
        status=Post.Status.PUBLISHED,
        slug = slug,
        publish__year = year,
        publish__month = month,
        publish__day = day
    )
    return render(
        request,
        'spotlightcentral/post/details.html',  # Corrected template name
        {'post': post}  # Corrected variable name
    )


class PostListView(ListView):
    '''
    Alternative post view list
    '''
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'spotlightcentral/post/list.html'
    # {% include "spotlightcentral/pagination.html" with page=page_obj %}  this should be added in the list.html incase we want to use the class base view
    


from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView

# Create your views here.

def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        posts = paginator.page(1 if isinstance(page_number, int) else paginator.num_pages)

    return render(request, 'spotlightcentral/post/list.html', {'posts': posts})

def post_details(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'spotlightcentral/post/details.html', {'post': post})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'spotlightcentral/post/list.html'

