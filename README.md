# smartcities
SmartCities data jam work: http://www.techoregon.org/event/global-smart-cities-hackathon-16529658654


MIT License

```py
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
```
