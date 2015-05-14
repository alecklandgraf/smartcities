"""Example usage:
    from models import load_first_100_into_elasticsearch
    from models import get_search_client
    from models import AIR_QUALITY_URL

    load_first_100_into_elasticsearch(AIR_QUALITY_URL, 'AirQuality')

    s_orig = get_search_client('AirQuality')
    s = s_orig.filter('term', epa_station_key=410350004)
    s.count()  # >>> 3
    hits = s.execute().hits()
    for h in hits:
        print h.dt_pst, h.temperature

    s_orig.aggs.metric('average_humidity', 'avg', field='relative_humidity')
    resp = s.execute()
    avg_humidity = resp.aggregations.average_humidity['value']  # 51.918338230
    resp.to_dict()  # {u'average_humidity': {u'value': 51.91833823076923}}

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
    'http://pdx.datadash.io/api/data/55353d09abadd8b7001497c4?limit=10000'
)


def load_first_100_into_elasticsearch(url, doc_type='AirQuality'):
    """Loads first 100 API responses into Elasticsearch"""
    data = requests.get(url).json()
    es = Elasticsearch()
    bulk(es, data, index=ES_INDEX, doc_type=doc_type, timeout=60)


def get_search_client(doc_type='AirQuality'):
    es = Elasticsearch()
    return Search(es, index=ES_INDEX, doc_type=doc_type)


# mapping look like this: TODO: map dt_pst into DateTime
# {u'mappings': {u'AirQuality': {u'properties': {u'_created_at':
#   {u'format': u'dateOptionalTime',
#      u'type': u'date'},
#     u'_updated_at': {u'format': u'dateOptionalTime', u'type': u'date'},
#     u'barometric_pressure': {u'type': u'double'},
#     u'carbon_monoxide': {u'type': u'double'},
#     u'delta_temperature': {u'type': u'double'},
#     u'dt_pst': {u'type': u'string'},
#     u'epa_station_key': {u'type': u'long'},
#     u'light_scatter': {u'type': u'double'},
#     u'nitric_oxide': {u'type': u'double'},
#     u'nitrogen_dioxide': {u'type': u'double'},
#     u'nitrogen_oxides': {u'type': u'double'},
#     u'ozone': {u'type': u'double'},
#     u'relative_humidity': {u'type': u'double'},
#     u'resultant_direction': {u'type': u'double'},
#     u'resultant_speed': {u'type': u'double'},
#     u'sd_hor_wind_dir': {u'type': u'double'},
#     u'solar_radiation': {u'type': u'long'},
#     u'sulfur_dioxide': {u'type': u'double'},
#     u'temperature': {u'type': u'double'},
#     u'wind_speed': {u'type': u'double'}}}}}
#
# a doc
# {u'_created_at': u'2015-04-20T17:53:13.181Z',
# u'_id': u'84',
# u'_updated_at': u'2015-04-20T17:53:13.181Z',
# u'barometric_pressure': 25.93,
# u'carbon_monoxide': u'',
# u'delta_temperature': 0.07,
# u'dt_pst': u'2015-02-22 00:10:00-08',
# u'epa_station_key': 410350004,
# u'light_scatter': 0.28,
# u'lower_level_temperature': u'',
# u'middle_level_temperature': u'',
# u'nitric_oxide': u'',
# u'nitrogen_dioxide': u'',
# u'nitrogen_oxides': u'',
# u'ozone': u'',
# u'relative_humidity': 55,
# u'resultant_direction': 34,
# u'resultant_speed': 12.8,
# u'sd_hor_wind_dir': 22.5,
# u'solar_radiation': u'',
# u'sulfur_dioxide': u'',
# u'temperature': 1.1,
# u'upper_level_temp': u'',
# u'wind_speed': 13.9}
