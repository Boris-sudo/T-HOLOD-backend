import os
from django.core.mail import send_mail
import datetime
import dotenv
from django.utils import timezone
import requests
import django
from celery import Celery

BASE_URL = "https://proverkacheka.com/api/v1/check/get"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcold.settings')

django.setup()

app = Celery('tcold')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.broker_connection_retry_on_startup = True

from django.conf import settings
from fridges.models import Fridge
from products.models import Product
from django.contrib.auth.models import User

dotenv.load_dotenv()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10,
        send_mail_.s(),
        name = "send mail"
    )


@app.task(bind=True)
def send_mail_():
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


STOP_WORDS = [
    "пакеты", "пакет"
]


@app.task()
def push_receipts(user_id: int, fridge_id: int, q: str):
    response = requests.post(BASE_URL, data={
        "token": settings.TOKEN,
        "qrraw": q
    })

    user = User.objects.get(id=user_id)
    fridge = Fridge.objects.get(id=fridge_id)

    if response.status_code > 299 and response.status_code < 200:
        return

    data = response.json()

    try:
        for product in data["data"]["json"]["items"]:
            stop_word = False
            for word in STOP_WORDS:
                if word not in product["name"].lower():
                    stop_word = True
            
            if stop_word:
                continue

        product_db = Product.objects.filter(
            name = product["name"]
        )

        print("Add")

        if product_db.exists():
            product_db = product_db.first()
            product_db.count += product["quantity"]
            product_db.save()
        else:
            product_db = Product.objects.create(
                name = product["name"],
                fridge = fridge,
                user = user,
                count = int(product["quantity"]),
                end_date = timezone.now() + datetime.timedelta(days=7)
            )
            product_db.save()
    except Exception as e:
        print(e)
        return
