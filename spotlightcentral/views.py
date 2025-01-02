from django.shortcuts import get_object_or_404,render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator
# Create your views here.


def post_list(request):
    post_list = Post.published.all()
    #doing a paginator with only 4 post per list
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)


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




