from django.dispatch import Signal

raw_hook_event = Signal(providing_args=['event_name', 'payload', 'user'])
