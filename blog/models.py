import os
from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Tag(models.Model):   # Tag 모델 정의
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    # unique :: 중복사용 안되게 처리 / allow_unicode :: 한글 처리

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/blog/tag/{self.slug}/"



class Category(models.Model):   # Category 모델 정의
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/blog/category/{self.slug}/"

    class Meta:
        verbose_name_plural = "categories"



class Post(models.Model):       # Post 모델 정의
    title = models.CharField(max_length=30)                     # .CharField() : 한줄 문장을 입력(<input> 타입)
    hook_text = models.CharField(max_length=100, blank=True)    # black=True : 해당 입력란에 null값 허용
#   content = models.TextField()                                # .TextField() : 여러줄의 문장을 입력할 수 있는 형식 (<textarea> 타입)
    content = MarkdownxField()                                  # MarkdownxField() : import한 markdownx를 사용하기 위한 형식 수정 (<textarea> 타입)


    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)   # 해당 프로젝트가 설치된 폴더 하위에 [_media] 폴더를 생성한 곳을 기본으로 이후 경로를 지정.
    file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)        # auto_now_add: 생성시간을 자동으로 저장
    updated_at = models.DateTimeField(auto_now=True)            # auto_now: 수정시간을 자동으로 저장
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  
                                                                # on_delete :: 해당 변수가 지워졌을 때 처리 방식 결정
                                                                #             (models.CASCADE: 연결된 것들은 삭제, models.SET_NULL: 변수 자리를 null로 처리)

    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    
    tags = models.ManyToManyField(Tag, blank=True)          # ManyToManyField ::: N-N 형식의 Field임을 설정. 

    def __str__(self):                      # 객체를 문자열로 표현할 때 사용
        return f'[{self.pk}] {self.title}'              # pk: 객체의 고유한 번호, title: 제목. 게시물의 기본키가 대괄호로
    
    def get_absolute_url(self):             # get_absolute_rul 메서드 정의
        return f'/blog/{self.pk}/'                       # 게시물의 상세 페이지 주소를 반환 (포스팅된 게시물의 페이지번호를 pk를 이용하여 자동으로 추가)

    def get_file_name(self):                # 업로드한 파일의 파일명 정의를 위한 메서드
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):                 # 업로드한 파일의 확장자 정의를 위한 메서드
        return self.get_file_name().split(".")[-1]      # 업로드된 파일의 파일명에서 .을 기준으로 잘라 뒤에서 첫번째 항목을 가져옴.
    
    def get_content_markdownx(self):
        return markdown(self.content)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)         # 원본글과 댓글은 연동되어야 하기에 cascade를 적용.
    author = models.ForeignKey(User, on_delete=models.CASCADE)       # 작성자와 댓글은 연동되어야 하기에 cascade를 적용.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    