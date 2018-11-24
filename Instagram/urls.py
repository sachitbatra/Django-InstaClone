from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from authentication.views import *
from photos.views import *
from chat.views import *
from django.conf.urls.static import static
from Instagram import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url('error', error),
    path('photos/post', post_view),
    path('photos/likes/<post_id>', view_likes),
    path('photos/like', like_view),
    path('photos/comment', comment_view),
    path('photos/feed', feed_view),
    path('photos/<email>', profile_view),
    path('photos/tag/<tag_name>', tag_view),
    path('chat', InboxView.as_view()),
    re_path(r"chat/(?P<username>[\w.@+-]+)/", ThreadView.as_view()),
    path('register/', user_signup),
    path('logout/', logout),
    path('', user_login),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
