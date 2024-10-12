from .models import Product


def check_product(request):
    id_product = request.data.get('id')

    if not id_product:
        return None

    product = Product.objects.filter(id=id_product)

    if not product.exists():
        return None
    
    return product.first()