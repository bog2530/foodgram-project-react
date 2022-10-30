from rest_framework import mixins, viewsets


class ReadingMixins(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass
