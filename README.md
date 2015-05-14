# smartcities
SmartCities data jam work: Python + Elasticsearch + D3

http://www.techoregon.org/event/global-smart-cities-hackathon-16529658654

#### Quick Start

For the python bits, start a `virtualenv`, clone the repo, then install the python reqs:

```console
virtualenv smartcities
git clone git@github.com:alecklandgraf/smartcities.git
cd smartcities
pip install -r requirements.txt
```

Get [Elasticearch](https://www.elastic.co/downloads/elasticsearch)  and start it up! Now you can load some data.

#### Getting the data into python and Elasticsearch

```py
from utils import load_first_100_into_elasticsearch
from utils import get_search_client
from utils import AIR_QUALITY_URL

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


MIT License
