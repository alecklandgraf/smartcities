"""Example usage:
    from utils import load_into_elasticsearch
    from utils import get_search_client
    from utils import AIR_QUALITY_URL

    load_into_elasticsearch(AIR_QUALITY_URL, 'AirQuality', limit=100)

    s_orig = get_search_client('AirQuality')
    s = s_orig.filter('term', epa_station_key=410350004)
    s.count()  # >>> 3
    hits = s.execute().hits()
    for h in hits:
        print h.dt_pst, h.temperature

    s_orig.aggs.metric('average_humidity', 'avg', field='relative_humidity')
    resp = s.execute()
    avg_humidity = resp.aggregations.average_humidity['value']  # 51.918338230
    resp.to_dict()  # {'average_humidity': {'value': 51.91833823076923}}

"""
import requests
# from datetime import datetime
# from elasticsearch_dsl import DocType, String, Date, Integer
# from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search

ES_INDEX = 'smartcities'
AIR_QUALITY_URL = (
    'http://pdx.datadash.io/api/data/55353d09abadd8b7001497c4'
)


def load_into_elasticsearch(url, doc_type='AirQuality', limit=100):
    """Loads first `limit` API responses into Elasticsearch"""
    url += '?limit={}'.format(limit)
    data = requests.get(url).json()
    es = Elasticsearch()
    bulk(es, data, index=ES_INDEX, doc_type=doc_type, timeout=60)


def get_search_client(doc_type='AirQuality'):
    es = Elasticsearch()
    return Search(es, index=ES_INDEX, doc_type=doc_type)


def check_mappings():
    """returns a dict of the Elasticsearch mapping within index `seedcities`"""
    es = Elasticsearch()
    mappings = es.indices.get_mapping().get('smartcities')
    print mappings
    return mappings


# mapping look like this: TODO: map dt_pst into DateTime
# {'mappings': {'AirQuality': {'properties': {'_created_at':
#   {'format': 'dateOptionalTime',
#      'type': 'date'},
#     '_updated_at': {'format': 'dateOptionalTime', 'type': 'date'},
#     'barometric_pressure': {'type': 'double'},
#     'carbon_monoxide': {'type': 'double'},
#     'delta_temperature': {'type': 'double'},
#     'dt_pst': {'type': 'string'},
#     'epa_station_key': {'type': 'long'},
#     'light_scatter': {'type': 'double'},
#     'nitric_oxide': {'type': 'double'},
#     'nitrogen_dioxide': {'type': 'double'},
#     'nitrogen_oxides': {'type': 'double'},
#     'ozone': {'type': 'double'},
#     'relative_humidity': {'type': 'double'},
#     'resultant_direction': {'type': 'double'},
#     'resultant_speed': {'type': 'double'},
#     'sd_hor_wind_dir': {'type': 'double'},
#     'solar_radiation': {'type': 'long'},
#     'sulfur_dioxide': {'type': 'double'},
#     'temperature': {'type': 'double'},
#     'wind_speed': {'type': 'double'}}}}}
#
# a doc
# {'_created_at': '2015-04-20T17:53:13.181Z',
# '_id': '84',
# '_updated_at': '2015-04-20T17:53:13.181Z',
# 'barometric_pressure': 25.93,
# 'carbon_monoxide': '',
# 'delta_temperature': 0.07,
# 'dt_pst': '2015-02-22 00:10:00-08',
# 'epa_station_key': 410350004,
# 'light_scatter': 0.28,
# 'lower_level_temperature': '',
# 'middle_level_temperature': '',
# 'nitric_oxide': '',
# 'nitrogen_dioxide': '',
# 'nitrogen_oxides': '',
# 'ozone': '',
# 'relative_humidity': 55,
# 'resultant_direction': 34,
# 'resultant_speed': 12.8,
# 'sd_hor_wind_dir': 22.5,
# 'solar_radiation': '',
# 'sulfur_dioxide': '',
# 'temperature': 1.1,
# 'upper_level_temp': '',
# 'wind_speed': 13.9}
