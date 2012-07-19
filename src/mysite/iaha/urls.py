from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'iaha.views.index'),
    url(r'^players/?$', 'iaha.views.players'),
    url(r'^games/?$', 'iaha.views.games'),
    url(r'^player/(?P<player_id>\d+)/?$', 'iaha.views.player_detail'),
)