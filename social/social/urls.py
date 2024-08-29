
from django.contrib import admin
from django.urls import path
from fb import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('profile/',views.ProfileView.as_view()),
    path('profile/<int:pk>/',views.ProfileView.as_view()),
    path('productsearch/',views.ProfileSearch.as_view()),
    path('post/',views.PostView.as_view()),
    path('post/<int:pk>/',views.PostView.as_view()),
    path('comment/',views.CommentView.as_view()),
    path('commentlist/',views.CommentList.as_view()),
    path('comment/<int:pk>/',views.CommentView.as_view()),
    path('follow/',views.FollowView.as_view()),
    path('follow/<int:user_id>/',views.FollowView.as_view()),
    path('feed/',views.FeedView.as_view()),
    path('FollowingListView/',views.FollowingListView.as_view())

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
