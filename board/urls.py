from django.urls import path, include
from django.conf.urls import url
from tastypie.api import Api

from .api import ServiceResource, CategoryResource, StatusResource, EventsResource
from .feeds import EventFeed
from .views import IndexView, ServiceView


v1_api = Api(api_name='v1')
v1_api.register(ServiceResource())
v1_api.register(CategoryResource())
v1_api.register(StatusResource())
v1_api.register(EventsResource())


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    url(
        r"^services/(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$",
        ServiceView.as_view(),
        name="service",
    ),
    url(
        r"^services/(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})$",
        ServiceView.as_view(),
        name="service",
    ),
    url(
        r"^services/(?P<slug>[-\w]+)/(?P<year>\d{4})$",
        ServiceView.as_view(),
        name="service",
    ),
    url(r"^services/(?P<slug>[-\w]+)$", ServiceView.as_view(), name="service"),
    url(r'^feed$', EventFeed(), name='feed'),
    url(r'^api/', include(v1_api.urls)),

]
