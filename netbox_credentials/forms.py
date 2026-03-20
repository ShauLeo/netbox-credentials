from django import forms

from dcim.models import Device
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)

from .models import Credential, DeviceCredential


# ── Credential ──────────────────────────────────────────────────────────────


class CredentialForm(NetBoxModelForm):
    """Create / edit a reusable credential."""

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Leave blank to keep the current password unchanged on edit.",
    )
    comments = CommentField()

    class Meta:
        model = Credential
        fields = ("name", "username", "password", "description", "comments", "tags")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill the password widget with a placeholder when editing
        if self.instance.pk and self.instance.password_is_set:
            self.fields["password"].widget.attrs["placeholder"] = "••••••••"

    def save(self, commit=True):
        instance = super().save(commit=False)
        pw = self.cleaned_data.get("password")
        if pw:
            instance.password = pw  # triggers encryption
        elif not instance.pk:
            instance.password = ""
        # On edit with blank password field → keep existing encrypted value
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CredentialFilterForm(NetBoxModelFilterSetForm):
    model = Credential
    tag = TagFilterField(model)

    name = forms.CharField(required=False)
    username = forms.CharField(required=False)


# ── DeviceCredential ────────────────────────────────────────────────────────


class DeviceCredentialForm(NetBoxModelForm):
    credential = DynamicModelChoiceField(queryset=Credential.objects.all())
    device = DynamicModelChoiceField(queryset=Device.objects.all())

    class Meta:
        model = DeviceCredential
        fields = ("credential", "device", "role", "tags")


class DeviceCredentialFilterForm(NetBoxModelFilterSetForm):
    model = DeviceCredential
    tag = TagFilterField(model)

    credential_id = DynamicModelChoiceField(
        queryset=Credential.objects.all(),
        required=False,
        label="Credential",
    )
    device_id = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device",
    )
    role = forms.CharField(required=False)


# ── Bulk-assign form (assign one credential to many devices at once) ────────


class BulkAssignForm(forms.Form):
    credential = DynamicModelChoiceField(queryset=Credential.objects.all())
    devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all())
    role = forms.CharField(max_length=100, required=False)
