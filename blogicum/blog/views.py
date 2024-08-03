from django.conf import settings
from django.shortcuts import render, get_object_or_404

from django.http import HttpRequest, HttpResponse

from .models import Post, Category


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()[:settings.POSTS_PER_PAGE]
    return render(request, 'blog/index.html',
                  context={'post_list': posts})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post.objects.all(), id=post_id, )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    posts = Post.objects.filter(category__slug=category_slug)
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    location_name = posts.first().location.name if (posts.exists()
                                                    and posts.first().location)\
                                                     else "Планета Земля"
    return render(request, 'blog/category.html', {
        'category': {
            'title': category.title,
            'slug': category.slug,
        },
        'post_list': posts,
        'location': {
            'name': location_name,
        },
    })