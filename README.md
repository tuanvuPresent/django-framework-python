# Django-framework-python
- [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- [https://docs.djangoproject.com/en/3.0/](https://docs.djangoproject.com/en/3.0/)

---
# Use
step 1: install docker and docker-compose

- [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
- [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

step 2: Build code with docker compose
```
docker-compose up --build
```

step 3: Run
```
- run server 0.0.0.0:8888

- run phpmyadmin 0.0.0.0:8088
```
---
# social-oauth2
```To get info user``` 
### Github
- access_token_github = 'abc'
- headers = {'Authorization': 'token {}'.format(access_token_github)}
- url1 = 'https://api.github.com/user'
- url2 = 'https://api.github.com/user/email'
- res1 = requests.get(url1, headers=headers)
- res2 = requests.get(url2, headers=headers)
- print('github', res1.json())
- print('github', res2.json())

### Facebook
- url = 'https://graph.facebook.com/v3.2/me'
- access_token_facebook = 'abc'
- params = {'access_token': access_token_facebook}
- res = requests.get(url, headers=headers, params=params)
- print('facebook', res.json())

### Google
- url = 'https://www.googleapis.com/oauth2/v3/userinfo'
- access_token_google = 'abc'
- headers = {'Authorization': 'Bearer {}'.format(access_token_google)}
- res = requests.get(url, headers=headers)
- print('google', res.json())

### Third-party application permissions for mail 
- https://myaccount.google.com/lesssecureapps


## Filter elasticsearch

- all

```
search = MyModel.objects.all()
search = MyModelDocument.search()
```

- Filter

```
queryset = queryset.filter(my_field__icontains=value)
search = search.filter('match_phrase', my_field=value)
```

```
queryset = queryset.filter(my_field__exact=value)
search = search.filter('match', my_field=value)
```

```python
from django.db import models

queryset = queryset.filter(
    models.Q(my_field=value) |
    models.Q(my_field2=value2)
)

from elasticsearch_dsl.query import Q

search = search.query(
    Q('match', my_field=value) |
    Q('match', my_field2=value2)
)
```

```python
from datetime import datetime

queryset = queryset.filter(
    published_at__lte=datetime.now(),
)

from datetime import datetime

search = search.filter(
    'range',
    published_at={'lte': datetime.now()}
)
```

aggregation

```python
query = {
    "size": 0,
    "aggs": {
        "avg_field": {
            "terms": {
                "field": "field_group_by"
            },
            "aggs": {
                "avg_field_name": {
                    "avg": {
                        "field": "field_name"
                    }
                },
            }
        }
    }
}
els.search(index=INDEX_ELS, **query)
```
```
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-weight-avg-aggregation.html
```

## Mongodb
- Install
```
pip install mongoengine==0.27.0
```
- Connect
``` 
connect(host=DATABASE_MONGO_URI)
```
- Document
```python
from mongoengine import Document, DynamicDocument
from mongoengine import fields


class Collection1(DynamicDocument):
    content = fields.StringField()

    meta = {
        'collection': 'collection',
    }

# or
class Collection2(Document):
    content = fields.StringField()

    meta = {
        'collection': 'collection',
        'strict': False,
    }
```
- Query
```python
# GET
query = Collection1.objects(content=?)
# Create
collection = Collection1(content=?)
collection.save()
# Count
count = Collection1.objects(content=?).count()
```
