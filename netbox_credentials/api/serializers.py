from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer

from ..models import Credential, DeviceCredential


class CredentialSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_credentials-api:credential-detail"
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="Write-only. Will be encrypted at rest.",
    )
    password_is_set = serializers.BooleanField(read_only=True)

    class Meta:
        model = Credential
        fields = (
            "id",
            "url",
            "display",
            "name",
            "username",
            "password",
            "password_is_set",
            "description",
            "comments",
            "tags",
            "created",
            "last_updated",
        )

    def create(self, validated_data):
        pw = validated_data.pop("password", "")
        instance = super().create(validated_data)
        if pw:
            instance.password = pw
            instance.save(update_fields=["_password"])
        return instance

    def update(self, instance, validated_data):
        pw = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if pw is not None and pw != "":
            instance.password = pw
            instance.save(update_fields=["_password"])
        return instance


class DeviceCredentialSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_credentials-api:devicecredential-detail"
    )

    class Meta:
        model = DeviceCredential
        fields = (
            "id",
            "url",
            "display",
            "credential",
            "device",
            "role",
            "tags",
            "created",
            "last_updated",
        )
