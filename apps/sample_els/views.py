from django_elasticsearch_dsl_drf.constants import LOOKUP_QUERY_CONTAINS
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, FilteringFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.sample_els.documents import SampleDocument
from apps.sample_els.serializer_document import SampleDocumentSerializer


class SampleDocumentApiView(DocumentViewSet):
    document = SampleDocument
    serializer_class = SampleDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'name',
    )

    filter_fields = {
        'name': {
            'field': 'name',
            'default_lookup': LOOKUP_QUERY_CONTAINS,
        },
    }
