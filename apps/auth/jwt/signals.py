from apps.auth.jwt.cache import UserActivityStore
from apps.auth.jwt.models import UserActivity
from django.dispatch import receiver
from django.dispatch import Signal

user_login = Signal(providing_args=['user'])
user_logout = Signal(providing_args=['user'])


@receiver(user_login)
def user_login_event(sender, user, **kwargs):
    UserActivity.objects.get_or_create(user=user, session_key=user.sid)


@receiver(user_logout)
def user_logout_event(sender, user, **kwargs):
    UserActivity.objects.filter(user=user, session_key=user.sid).delete()
    UserActivityStore(user).logged_out()
