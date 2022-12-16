from datetime import date
from apps.shops.models import Revenue, Order
from Example.celery import app


@app.task()
def scheduled_update_revenue():
    today = date.today()
    revenue, is_created = Revenue.objects.get_or_create(
        date=today
    )

    queryset = Order.objects.filter(is_pay=True, date_pay=today)
    total = 0
    for order in queryset:
        try:
            amount = int(order.total_amount)
        except ValueError:
            amount = 0
        total += amount

    revenue.total = total
    revenue.save()
