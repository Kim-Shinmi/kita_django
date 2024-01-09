from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView           # 사용자 화면에서 CRUD를 진행하기 위한 클래스 import
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Post, Category, Tag, Comment                # DB와의 연동을 위해 생성한 Post, Category, Tag 클래스 import
from .forms import CommentForm
from django.utils.text import slugify                           # slugify :: 문자열을 URL에 적합한 형태로 변환
from django.shortcuts import get_object_or_404                  # get_object_or_404 :: 해당 객체가 존재하지 않을 경우 404 오류 페이지를 반환
from django.core.exceptions import PermissionDenied             # PermissionDenied :: 발생한 오류에 대한 예외처리 관련 
from django.db.models import Q                                  # Q :: DB에서 데이터를 검색 또는 필터링 시, 다양한 조건을 조합하고 동적으로 쿼리를 작성하는 상황에서 유용



# CBV(Class Based View) 방식 : Class 기반의 View 생성
class PostList(ListView):           # post_list.html 파일 출력을 위한 class (PostList는 Listview를 상속받음.)
    model = Post
    ordering = "-pk"
    paginate_by = 5                          # 리스트에서 페이징 처리를 하기 위한 부분 (Post 갯수가 5개를 기준으로 페이징 처리)

    def  get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()      # Category 선택이 안된 것은 미분류로...
        return context



class PostDetail(DetailView):       # post_detail.html 파일 출력을 위한 class (PostDetail은 DetailView를 상속받음.)
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm               # 필요에 따라 객체를 만들어 쓸 수 있게 클래스를 이용
        return context
    


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]         # field의 항목은 models.py에서 정의한 항목들을 사용

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user                         # 사용자는 수퍼관리자(is_superuser)와 관리자(is_staff)
        # return self.request.user.is_superuser or self.request.user.is_staff or self.request.user      # 사용자는 수퍼관리자(is_superuser)와 관리자(is_staff), 일반 유저(user)
        # return self.request.user      # 사용자는 수퍼관리자(is_superuser)와 관리자(is_staff), 일반 유저(user)
    
    def form_valid(self, form):                     # form_valid 메서드 :: Form 데이터가 유효할 때 호출되는 메서드
        current_user = self.request.user

        # if current_user.is_authenticated and (                          # 현재 사용자가 로그인 한 사용자(is_authenticated) 이면서
        #    current_user.is_staff or current_user.is_superuser          #              관리자(is_staff)거나 수퍼관리자(is_superuser)일 때
        # ):
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get("tags_str")                # tags_str : 태그를 입력하는 폼에서 전달받은 데이터               

            if tags_str:
                tags_str  = tags_str.strip()

                tags_str = tags_str.replace(",", ";")                   # ','는 db에서 사용되는 구분자 (∵ 오류 방지를 위해 ','를 ';'로 변환처리)
                tags_list = tags_str.split(";")

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)

                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode = True)
                        tag.save()

                    self.object.tags.add(tag)
                    
            return response
        else:
            return redirect("/blog/")
    

    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]

    template_name = "blog/post_update_form.html"

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()

        if self.object.tags.exists():
            tags_str_list = list()

            for t in self.object.tags.all():
                tags_str_list.append(t.name)

            context["tags_str_default"] = "; ".join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get("tags_str")

        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(",", ";")
            tags_list = tags_str.split(";")

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)

                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()

                self.object.tags.add(tag)

        return response


    
def category_page(request, slug):    # slug는 일반적으로 이미 얻은 데이터를 사용하여 유효한 url을 생성
    if slug == "no_category":
        category = "미분류"
        post_list = Post.objects.filter(category = None)
    else:
        category = Category.objects.get(slug = slug)
        post_list = Post.objects.filter(category = category)

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list" : post_list,
            "categories" : Category.objects.all(),
            "no_category_post_count" : Post.objects.filter(category=None).count(),
            "category" : category,              # 현재 선택된 카테고리
        }
    )



def tag_page(request, slug): 
    tag = Tag.objects.get(slug = slug)      # 해당 slug와 일치하는 Tag 객체를 가져옴
    post_list = tag.post_set.all()          # tag에 속한 모든 Post 객체를 가져옴 

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list" : post_list,        # 게시물 목록을 템플릿에 전달하여 해당 태그에 속한 게시물만 출력
            "categories" : Category.objects.all(),          # 모든 카테고리 정보를 가져와 템플릿에 전달
            "no_category_post_count" : Post.objects.filter(category=None).count(),
            "tag" : tag,                    # 현재 선택된 태그
        }
    )



def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)           # pk에 해당하는 Post 객체를 가져옴

        if request.method == "POST":
            comment_form = CommentForm(request.POST)    # CommentForm(request.POST)를 사용하여 제출된 데이터로 댓글 폼의 인스턴스를 생성

            if comment_form.is_valid():                     # 폼의 데이터가 유효한지 검사
                comment = comment_form.save(commit=False)       # comment 객체를 생성하되, 데이터베이스에는 저장하지 않음.(commit=False)
                comment.post = post                             # 댓글 객체에 post 속성을 할당
                comment.author = request.user                   # 댓글 객체에 author 속성을 할당
                comment.save()

                return redirect(comment.get_absolute_url()) # 댓글 객체의 get_absolute_url 메서드를 호출하여 댓글 상세 페이지로 이동
                
        else:
            return redirect(post.get_absolute_url())    # 댓글 폼이 유효하지 않으면 post.get_absolute_url()로 이동
    else:
        raise PermissionDenied                  # 로그인하지 않은 사용자가 댓글을 작성하려고 하면 PermissionDenied 예외를 발생시킴



class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment                             # Comment 모델을 사용
    form_class = CommentForm                    # 사용할 폼으로 CommentForm을 지정

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()

        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    


class PostSearch(PostList):
    paginate_by = None                          # 리스트에서 페이징 처리를 하기 위한 부분 (None으로 표현되어 있기에 페이징 처리 안됨.)

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)    # 장고에서의 쿼리 표현식 (단어를 __로 연결해 줌)
        ).distinct()                                            # .distinct() : 중복 제거 함수 (검색 결과의 중복된 내용을 제거)

        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context
    


# FBV(Function Based View) 방식 : 함수 기반의 View 생성
# def index(request):
#     posts = Post.objects.all().order_by('-pk')      # 모든 Post 객체를 가져와서 정렬 ('-pk' : pk 역순정렬)
#     return render(          # render 함수는 세 번째 인수로 전달된 딕셔너리 데이터를 템플릿 파일에 적용하여 HTML 코드로 변환
#         request,                    # 첫 번째 인수: 반드시 request
#         'blog/index.html',          # 두 번째 인수: 템플릿 파일의 경로
#         {                           # 세 번째 인수(블록으로 표기)
#             'posts' : posts,                # posts 키에 posts 변수를 할당
#         }
#     )

# def single_post_page(request, pk):                  # pk 인자: URL에서 추출한 게시물의 고유 번호
#     post = Post.objects.get(pk=pk)          # pk가 매개변수 pk와 같은 Post 객체를 post 변수에 할당

#     return render(
#         request,
#         'blog/single_post_page.html',       # 템플릿 파일의 경로
#         {
#             'post': post,
#         }
#     )


