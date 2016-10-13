from product_management.serializers import ShoesSerializer, MobilesSerializer
from . import Product, Mobiles, Shoes


class ProductManager(object):

    def __init__(self):
        self.start = 0
        self._offset = None

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = None if value is None else value + self.start
    
    @property
    def product_ids(self):
        return Product.objects.values_list('id')

    @property
    def fields(self):
        return [f.name for f in Product._meta.get_fields()]

    @property
    def categories(self):
        return Product.objects.order_by().values_list('category').distinct()

    def _process_filters(self, filter_dict):
        # Add `product__<filter_key>` in case of filters that belongs
        # to `Product` model
        fields = self.fields
        tmp_dict = {}
        for key, value in filter_dict.iteritems():
            if key in fields:
                tmp_dict['product__' + key] = value
            else:
                tmp_dict[key] = value
        return tmp_dict

    def validate_filters(self, request, **kw):
        # Boolean filters possible values 0/1
        # More filters can be added here
        self.start = request.GET.get('start', 0)
        self.offset = request.GET.get('count')

        featured = request.GET.get('featured')
        in_stock = request.GET.get('in_stock')
        if featured is not None:
            kw['featured'] = featured
        if in_stock is not None:
            kw['in_stock'] = in_stock
        return kw

    def find(self, **kwargs):
        """Find all the categories data when requested for all products
        
        :param kwargs: Keywords of filter values.

        :return: A dict of serialized category data.
        """
        kwargs = self._process_filters(kwargs)
        mobiles = Mobiles.objects.filter(
            product_id__in=self.product_ids, **kwargs
            ).order_by('id')[self.start:self.offset]
        shoes = Shoes.objects.filter(
            product_id__in=self.product_ids, **kwargs
            ).order_by('id')[self.start:self.offset]
        # Serialize
        mob_serializer = MobilesSerializer(mobiles, many=True)
        shoe_serializer = ShoesSerializer(shoes, many=True)
        return dict(shoes=shoe_serializer.data, mobiles=mob_serializer.data)


