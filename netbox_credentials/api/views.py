from netbox.api.viewsets import NetBoxModelViewSet

from ..models import Credential, DeviceCredential
from ..filtersets import CredentialFilterSet, DeviceCredentialFilterSet
from .serializers import CredentialSerializer, DeviceCredentialSerializer


class CredentialViewSet(NetBoxModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    filterset_class = CredentialFilterSet


class DeviceCredentialViewSet(NetBoxModelViewSet):
    queryset = DeviceCredential.objects.select_related("credential", "device")
    serializer_class = DeviceCredentialSerializer
    filterset_class = DeviceCredentialFilterSet
