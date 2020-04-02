from rest_framework import serializers
from store.models import Product
from store.models import ShoppingCartItem

class CartItemSerializers(serializers.ModelSerializer):
    qunatity = serializers.IntegerField(min_value=1,max_value=10000)
    class Meta: 
        model = ShoppingCartItem
        fields= ('product','quantity')


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only = True)
    current_price = serializers.FloatField(read_only = True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()
    price = serializers.DecimalField(min_value=1.00,max_value=10000,max_digits=None,decimal_places=2,)
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only=True,default=None)
    class Meta:
        model= Product
        fields=('id','name','description','price','sale_start',
                'sale_end','is_on_sale','current_price','cart_items','photo','warranty')
        
    def get_cart_items(self,instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializers(items,many= True).data
    
    def update(self,instance,validated_data):
        if validated_data.get('warranty',None):
            instance.description+='\n\nWarranty Information:\n'
            instance.description+=b'; '.join(validated_data['warranty'].readlines()).decode()
        return instance
        
    # def to_representation(self,instance):
    #     data=super().to_representation(instance)
    #     data['is_on_sale'] = instance.is_on_sale()
    #     data['current_price'] = instance.current_price()
    #     return data   