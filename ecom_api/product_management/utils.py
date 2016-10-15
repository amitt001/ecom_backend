"""Simple utility methods for product_management views"""

from .models import Shoes, Product, Mobiles
from .serializers import ShoesSerializer, MobilesSerializer


# Model routing factory based on category
def model_factory(category):
    return {
        'shoes': Shoes,
        'mobiles': Mobiles,
    }[category.lower()]

# Serializer routing factory based on category
def serializer_factory(category):
    return {
        'shoes': ShoesSerializer,
        'mobiles': MobilesSerializer,
    }[category.lower()]

# converts a nested dict to top level dict
# Supports both list of dicts or a dict
def top_level_dict(data):
    """If dict comes i.e. single value return dict

    if a list comes i.e. many values return a list of dict"""
    data_is_dict = isinstance(data, dict)
    if not data:
        return {} if data_is_dict else []
    if data_is_dict:
        data = [data]
    top_level = []
    for dct in data:
        tmp = {}
        for key, value in dct.iteritems():
            if isinstance(value, dict):
                tmp.update(value)
            else:
                tmp[key] = value
        top_level.append(tmp)
    return tmp if data_is_dict else top_level


# Add a navigable hyperlink for each resource
def add_hyperlink(request, data):
    data_is_dict = isinstance(data, dict)
    if not data:
        return {} if data_is_dict else []
    uri = request.build_absolute_uri().split('?')[0].rstrip('/')
    # if data_is_dict:
    #     mod_data = {'data': data}
    #     # Handle casses when category already in uri
    #     if data['category'].lower() not in uri:
    #         uri += '/' + data['category'].lower() + 's'
    #     mod_data['url'] = '{}/{}'.format(uri, data['id'])
    # else:
    # If data is a dict i.e. a single resource do not add url
    if not data_is_dict:
        mod_data = []
        for d in data:
            tmp = {'data': d}
            if d['category'].lower() not in uri.lower():
                uri += '/' + d['category'].lower()
            tmp['url'] = '{}/{}'.format(uri, d['id'])
            mod_data.append(tmp)
    return data if data_is_dict else mod_data
