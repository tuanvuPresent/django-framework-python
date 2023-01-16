from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from apps.sample_els.models import Sample


@registry.register_document
class SampleDocument(Document):
    class Index:
        name = 'sample'

    class Django:
        model = Sample

        fields = [
            'id',
            'name',
        ]
