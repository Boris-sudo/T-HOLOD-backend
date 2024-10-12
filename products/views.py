from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from fridges.utils import get_user_from_request
from fridges.utils import check_fridge, check_user
from fridges.models import Fridge
from .serializers import ProductSerializer, ProductCreateSetializer
from .models import Product
from .utils import check_product


class ProductViewSet(ViewSet):

    def validate_product(self, request, pk):
        user = get_user_from_request(request)
        fridge = check_fridge(pk)
        product: Product = check_product(request)

        if not product:
            return Response({
                "error": "no such product!"
            })

        if not fridge or not fridge.members.contains(user):
            return Response({
                "error": "no such fridge!"
            }, status=404)
        
        return product, fridge, user

    @action(methods=["GET"], detail=True)
    def get_products_by_fridge(self, request, pk = None):
        user = get_user_from_request(request)

        fridge: Fridge = check_fridge(pk)

        if not fridge and not fridge.members.contains(fridge):
            return Response({
                "error": "no such fridge!"
            }, status=404)
        
        product = Product.objects.filter(fridge=fridge)

        return Response(
            ProductSerializer(product, many=True).data
        )
    
    def create(self, request):
        user = get_user_from_request(request)

        product_serializer = ProductCreateSetializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save(user, product_serializer.validated_data)

        if not product:
            return Response({
                "error": "no such fridge!"
            }, status=403)
        
        return Response(
            ProductSerializer(instance=product).data
        )
        
    @action(methods=["POST"], detail=True)
    def decrement_product(self, request, pk = None):
        response = self.validate_product(request, pk)

        if isinstance(response, Response):
            return response
        
        product, _, _ = response

        product.count -= 1
        if product.count <= 0:
            product.delete()
        else:
            product.save()

        return Response(
            ProductSerializer(instance=product).data
        )
    
    @action(methods=["POST"], detail=True)
    def increment_product(self, request, pk = None):
        response = self.validate_product(request, pk)

        if isinstance(response, Response):
            return response
        
        product, _, _ = response

        product.count += 1
        product.save()

        return Response(
            ProductSerializer(instance=product).data
        )
    
    @action(methods=["DELETE"], detail=True)
    def remove_product(self, request, pk = None):
        response = self.validate_product(request, pk)

        if isinstance(response, Response):
            return response
        
        product, _, _ = response

        product.delete()

        return Response(
            ProductSerializer(instance=product).data
        )
    
    @action(methods=["DELETE"], detail = True)
    def clear_fridge(self, request, pk = None):
        user = get_user_from_request(request)
        fridge: Fridge = check_fridge(pk)

        if not fridge:
            return Response({
                "error": "no such fridge!"
            }, status=404)
        
        if not fridge.members.contains(user) or fridge.owner != user:
            return Response({
                "error": "you cannot to do that!"
            })

        products = Product.objects.filter(id=fridge.id)

        for p in products:
            p.delete()
        
        return Response({
            "message": "ok"
        })
