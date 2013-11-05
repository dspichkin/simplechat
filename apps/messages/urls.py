from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.messages.views import Messages, Chat


urlpatterns = patterns(
    '',
    url(r'^$', login_required(Messages.as_view()), name='messages'),
    url(r'^(?P<pk>\d+)/$', login_required(Chat.as_view()), name='chat')
)
