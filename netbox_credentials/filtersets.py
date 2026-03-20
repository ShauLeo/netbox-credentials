import django_filters

from dcim.models import Device
from netbox.filtersets import NetBoxModelFilterSet

from .models import Credential, DeviceCredential


class CredentialFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Credential
        fields = ("id", "name", "username")


class DeviceCredentialFilterSet(NetBoxModelFilterSet):
    credential_id = django_filters.ModelChoiceFilter(
        queryset=Credential.objects.all(),
        label="Credential",
    )
    device_id = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device",
    )
    role = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = DeviceCredential
        fields = ("id", "credential_id", "device_id", "role")
