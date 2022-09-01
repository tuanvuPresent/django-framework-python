from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('e-learning/', include('apps.e_learning.exams.urls')),
    url('e-learning/', include('apps.e_learning.questions.urls')),
]