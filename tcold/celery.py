import os
from django.core.mail import send_mail
import datetime
import dotenv
import django
from celery.utils.log import get_task_logger
from django.utils import timezone

from celery import Celery

logger = get_task_logger(__name__)

dotenv.load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcold.settings')

django.setup()

app = Celery('tcold')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.broker_connection_retry_on_startup = True

from django.conf import settings
from fridges.models import Fridge
from products.models import Product

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10,
        send_mail_.s(),
        name = "send mail"
    )


@app.task(bind=True)
def send_mail_():
    logger.warning("RUN")

    products = Product.objects.filter(
        end_date__lte = timezone.now() - datetime.timedelta(days=7)
    )

    for product in products:
        for user in product.fridge.members.all():
            if user.email:
                send_mail(
                    "Сроки годности продукта подходят к концу",
                    f"Сроки годности продукта: {product.name} подходят к концу",
                    settings.EMAIL,
                    [user.email],
                    fail_silently=True
                )

# send_mail("Сроки годности продукта подходят к концу", f"Сроки годности продукта: подходят к концу", settings.EMAIL, ["as.voronin777@mail.ru"], fail_silently=True)