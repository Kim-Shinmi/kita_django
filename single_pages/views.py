from django.shortcuts import render
from blog.models import Post

# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]             # 가장 최신글 3개만 정렬

    return render(
        request, 
        'single_pages/landing.html',
        {
            'recent_posts' : recent_posts,
        }
    )  


def about_me(request):
    return render(request, "single_pages/about_me.html")       # html 파일의 경로이기 때문에 [single_pages] 폴더의 상위에 [templates] 폴더가 있어야 함.

