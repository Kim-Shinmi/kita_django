import os
from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/tag/{self.slug}/"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/category/{self.slug}/"

    class Meta:
        verbose_name_plural = "categories"


class Post(models.Model):  # Post 모델 정의
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    # content = models.TextField()
    content = MarkdownxField()

    head_image = models.ImageField(
        upload_to="blog/images/%Y/%m/%d/", blank=True
    )  # 필수항목은 아니다.
    file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자가 삭제되면 작성자명을 빈칸으로 둔다.
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):  # 객체를 문자열로 표현할 때 사용
        return f"[{self.pk}]{self.title}"  # pk: 객체의 고유한 번호, title: 제목. 게시물의 기본 키가 대괄호로 묶인 문자열을 출력하고 바로 뒤에 게시물 제목이 표시

    def get_absolute_url(self):  # get_absolute_url 메서드 정의
        return f"/blog/{self.pk}/"  # 게시물의 상세 페이지 주소를 반환

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)  # 파일명만 반환

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]  # 파일 확장자만 반환

    def get_content_markdownx(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}::{self.content}"

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"