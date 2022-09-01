from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('sample/', include('apps.sample.book.urls')),
    url('sample/', include('apps.sample.timesheet.urls')),
    url('sample/', include('apps.sample.todos.urls')),
]