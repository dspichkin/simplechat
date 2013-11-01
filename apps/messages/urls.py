from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.messages.views import Messages, SendMessage


urlpatterns = patterns(
    '',
    url(r'^$', login_required(Messages.as_view()), name='messages'),
    url(r'^$', login_required(SendMessage.as_view()), name='send_messages')
)
