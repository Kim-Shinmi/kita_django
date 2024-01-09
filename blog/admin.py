from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment    # models.py에서 등록한 클래스들을 import

# Register your models here.
admin.site.register(Post, MarkdownxModelAdmin)                           # Post 모델을 관리자 페이지에서 볼 수 있도록 등록



class CategoryAdmin(admin.ModelAdmin):          # ModelAdmin을 상속받아 사용.
    prepopulated_fields = {"slug" : ("name",)}      # name에 따라 slug가 생성될 수 있도록 커스터마이징 처리 (slug와 name의 관계를 튜플로 생성함. (∵ 데이터 변경을 막기 위해서))

admin.site.register(Category, CategoryAdmin)    # Category 모델을 커스터마이징 처리한 CategoryAdmin을 등록



class TagAdmin(admin.ModelAdmin):          # ModelAdmin을 상속받아 사용.
    prepopulated_fields = {"slug" : ("name",)}      # name에 따라 slug가 생성될 수 있도록 커스터마이징 처리 (slug와 name의 관계를 튜플로 생성함. (∵ 데이터 변경을 막기 위해서))

admin.site.register(Tag, TagAdmin)    # Category 모델을 커스터마이징 처리한 CategoryAdmin을 등록

