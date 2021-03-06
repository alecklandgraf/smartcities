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
EPA_STATION_URL = 'http://pdx.datadash.io/api/data/552d2910d838c1a200fa6927'


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


def drop_index():
    es = Elasticsearch()
    es.indices.delete(index=ES_INDEX)


def create_index():
    es = Elasticsearch()
    es.indices.create(index=ES_INDEX, ignore=400)


def reset_elasticsearch():
    drop_index()
    create_index()


def create_mappings(mapping_dict=None, doc_type='AirQuality'):
    es = Elasticsearch()
    mapping_dict = mapping_dict or get_default_mapping(doc_type)
    es.indices.put_mapping(
        index=ES_INDEX,
        doc_type=doc_type,
        body=mapping_dict
    )


def get_default_mapping(doc_type='AirQuality'):
    return {
        'AirQuality': {
            'properties': {
                '_created_at': {'format': 'dateOptionalTime', 'type': 'date'},
                '_updated_at': {'format': 'dateOptionalTime', 'type': 'date'},
                'barometric_pressure': {'type': 'double'},
                'carbon_monoxide': {'type': 'double'},
                'delta_temperature': {'type': 'double'},
                'dt_pst': {  # '2015-02-22 00:10:00-08'
                    'type': 'date',
                    'format': (
                        'yyyy-MM-dd HH:mm:ssZ||'
                        'date_optional_time'
                    ),
                    'ignore_malformed': True,  # force invalid values to null
                    'doc_values': True,
                },
                'epa_station_key': {'type': 'long'},
                'light_scatter': {'type': 'double'},
                'nitric_oxide': {'type': 'double'},
                'nitrogen_dioxide': {'type': 'double'},
                'nitrogen_oxides': {'type': 'double'},
                'ozone': {'type': 'double'},
                'relative_humidity': {'type': 'double'},
                'resultant_direction': {'type': 'double'},
                'resultant_speed': {'type': 'double'},
                'sd_hor_wind_dir': {'type': 'double'},
                'solar_radiation': {'type': 'long'},
                'sulfur_dioxide': {'type': 'double'},
                'temperature': {'type': 'double'},
                'wind_speed': {'type': 'double'}
            }
        }
    }
