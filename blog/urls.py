from django.urls import path
from . import views

# FBV(Function Based View) 방식
# urlpatterns = [
#     path('<int:pk>/', views.single_post_page),         # <int:pk> ::: pk가 정수형임을 명시
#     path('', views.index),                             # blog 앱에서의 기본(메인) 페이지
# ]


# CBV(Class Based View) 방식
urlpatterns = [
    path("<int:pk>/", views.PostDetail.as_view()),          # <int:pk> ::: pk가 정수형임을 명시
    path("", views.PostList.as_view()),                     # blog 앱에서의 기본(메인) 페이지
    path("category/<str:slug>/", views.category_page),      # category_page 처리를 위한 path 등록
    path("tag/<str:slug>/", views.tag_page),                # tag_page 처리를 위한 path 등록
    path('search/<str:q>/', views.PostSearch.as_view()),    # 리스트에서 검색을 위한 path 등록

    path("create_post/", views.PostCreate.as_view()),               # 사용자 화면에서 post 작성을 위한 페이지로 이동하는 path
    path("update_post/<int:pk>/", views.PostUpdate.as_view()),      # 작성된 post를 사용자 화면에서 수정하기 위한 페이지로 이동하는 path

    path("<int:pk>/new_comment/", views.new_comment),                   # 코멘트(댓글) 추가를 위한 path
    path("update_comment/<int:pk>/", views.CommentUpdate.as_view()),    # 코멘트(댓글) 수정을 위한 path
    path("delete_comment/<int:pk>/", views.delete_comment),             # 코멘트(댓글) 삭제를 위한 path
]
