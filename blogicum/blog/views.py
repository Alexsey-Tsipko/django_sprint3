from django.conf import settings
from django.shortcuts import render, get_object_or_404

from .models import Post, Category


def index(request):
    posts = Post.objects.all()[:settings.POSTS_PER_PAGE]
    return render(request, 'blog/index.html',
                  context={'post_list': posts})


def post_detail(request, post_id: int):
    post = get_object_or_404(Post.objects.all(), id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    posts = category.posts.filter(is_published=True)

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': posts,
    })
