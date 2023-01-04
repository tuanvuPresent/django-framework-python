from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.sendmail.serializer import SendEmailSerializer
from apps.common.custom_model_view_set import BaseGenericViewSet


class SendEmailAPIView(BaseGenericViewSet):

    @swagger_auto_schema(request_body=SendEmailSerializer)
    @action(methods=['post'], detail=False)
    def send_mail(self, request):
        data = request.data
        subject = data.get('subject', '')
        message = data.get('message', '')
        to_email = data.get('to_email', '')
        list_email = ['drf.server@gmail.com', to_email]
        try:
            send_mail(subject, message, 'drf.server@gmail.com', list_email,
                      fail_silently=False)
        except Exception as e:
            print(e)
        # file = request.FILES['file']
        # subject, from_email, to = 'hello', '', 'tuanvubk96@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach(file.name, file.read())
        # msg.send()

        return Response()
