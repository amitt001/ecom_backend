from .models import Shoes, Product, Mobile
from .serializers import (
    ProductSerializer, ShoesSerializer, MobileSerializer)

# Model routing factory based on category
def model_factory(category):
    return {
        'shoes': Shoes,
        'mobiles': Mobile,
    }[category]

# Serializer routing factory based on category
def serializer_factory(category):
    return {
        'shoes': ShoesSerializer,
        'mobiles': MobileSerializer,
    }[category]

# converts a nested dict to top level dict
# Supports both list of dicts or a dict
def top_level_dict(data):
    top_level = []
    if isinstance(data, dict):
        data = [data]
    for dct in data:
        tmp = {}
        for key, value in dct.iteritems():
            if isinstance(value, dict):
                tmp.update(value)
            else:
                tmp[key] = value
        top_level.append(tmp)
    else:
        return top_level if len(top_level) > 1 else tmp
    # Handle case when data is empty i.e. []
    return {} if not data else tmp


# Add a navigable hyperlink for each resource
def add_hyperlink(request, data):
    uri = request.build_absolute_uri().rstrip('/')
    if isinstance(data, dict):
        mod_data = {'data': data}
        if data['category'].lower() not in uri:
            uri += '/' + data['category'].lower() + 's'
        mod_data['url'] = '{}/{}'.format(uri, data['id'])
    else:
        mod_data = []
        for d in data:
            tmp = {'data': d}
            if d['category'].lower() not in uri:
                uri += '/' + d['category'].lower() + 's'
            tmp['url'] = '{}/{}'.format(uri, d['id'])
            mod_data.append(tmp)
    return mod_data