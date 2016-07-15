from django.conf.urls import include, url
import views
urlpatterns=[
    url(r'^secret',views.handle_secret),
    url(r'^message',views.handle_message)
]