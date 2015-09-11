from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

from rest_framework import filters
import django_filters

from core.models import ApplicationVersion as ImageVersion
from core.models import AccountProvider
from core.query import only_current_machines_in_version, only_current

from api.v2.views.base import AuthOptionalViewSet
from api.v2.serializers.details import ImageVersionSerializer


def get_admin_image_versions(user):
    """
    TODO: This 'just works' and is probably very slow... Look for a better way?
    """
    provider_id_list = user.identity_set.values_list('provider', flat=True)
    account_providers_list = AccountProvider.objects.filter(
        provider__id__in=provider_id_list)
    admin_users = [ap.identity.created_by for ap in account_providers_list]
    version_ids = []
    for user in admin_users:
        version_ids.extend(
            user.applicationversion_set.values_list('id', flat=True))
    admin_list = ImageVersion.objects.filter(
        id__in=version_ids)
    return admin_list


class ImageFilter(django_filters.FilterSet):
    image_id = django_filters.CharFilter('application__id')
    created_by = django_filters.CharFilter('application__created_by__username')

    class Meta:
        model = ImageVersion
        fields = ['image_id', 'created_by']


class ImageVersionViewSet(AuthOptionalViewSet):

    """
    API endpoint that allows instance actions to be viewed or edited.
    """
    queryset = ImageVersion.objects.all()
    serializer_class = ImageVersionSerializer
    search_fields = ('application__id', 'application__created_by__username')
    ordering_fields = ('start_date',)
    ordering = ('start_date',)
    filter_class = ImageFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)

    def get_queryset(self):
        request_user = self.request.user
        return ImageVersion.current_machines(request_user)
