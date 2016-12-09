from django.conf.urls import include, url
from django.contrib import admin

from .views import ChatterBotAppView,ChatterBotView

app_name='Capa'
urlpatterns = [
    url(r'^$', ChatterBotAppView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chatterbot/',ChatterBotView.as_view(),name="chatterbot"),
]

