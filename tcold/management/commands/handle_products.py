from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import datetime
from django.utils import timezone

from django.conf import settings
from products.models import Product


class Command(BaseCommand):
    help = "Starts handle products end_date"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
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