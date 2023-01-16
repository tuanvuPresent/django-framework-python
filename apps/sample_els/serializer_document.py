from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from apps.sample_els.documents import SampleDocument


class SampleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = SampleDocument

        fields = (
            'name',
            'id'
        )
