from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from .permissions import SuperUserOrAdmin, AnonimReadOnly


class CreateRetrieveDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для работы с моделями Genre, Category."""
    permission_classes = [SuperUserOrAdmin | AnonimReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
