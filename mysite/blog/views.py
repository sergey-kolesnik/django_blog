from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
    )
from django.http import Http404

from django.views.generic import ListView
from django.shortcuts import (
    render, 
    get_object_or_404
    )

from .models import Post
from .forms import EmailPostForm

# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get("page", 1)
#     try:

#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(
#         request,
#         "blog/post/list.html",
#         {"posts": posts}
#     )


class PostListView(ListView):
    """Альтернативное представление списка постов"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

def post_detail(request, year, month, day, post):
    print("qwertyyyyyyyyyyyyyyyy")
    post = get_object_or_404(
    Post,
    status=Post.Status.PUBLISHED,
    slug=post,
    publish__year=year,
    publish__month=month,
    publish__day=day,
    )

    return render(
        request,
        "blog/post/detail.html",
        {"post": post}
    )


def post_share(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )

    if request.method == "POST":

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

        else:
            form = EmailPostForm()

        return render(
            request,
            "blog/post/share.html",
            {
                "post": post,
                "form": form,
            }
        )

