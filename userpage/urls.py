from userpage import views
from django.urls import path

urlpatterns = [
    path('',views.userHome,name="userHome"),
    path('post',views.post,name="post"),
    path('like_dislike/<int:ID>',views.likePost,name="like_dislike_post"),
    path("<int:pk>/comment",views.comment,name="comment"),
    path('delete/<int:ID>',views.delPost,name="delPost"),
    path("<str:username>",views.userProfile,name='userProfile'),
    path('user/follow/<str:username>',views.follow,name="follow"),
    path('search/', views.SearchUser.as_view() , name='search_user')
]
