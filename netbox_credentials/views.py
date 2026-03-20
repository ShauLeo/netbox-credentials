from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from netbox.views import generic

from .filtersets import CredentialFilterSet, DeviceCredentialFilterSet
from .forms import (
    BulkAssignForm,
    CredentialFilterForm,
    CredentialForm,
    DeviceCredentialFilterForm,
    DeviceCredentialForm,
)
from .models import Credential, DeviceCredential
from .tables import CredentialTable, DeviceCredentialTable


# ── Credential views ────────────────────────────────────────────────────────


class CredentialListView(generic.ObjectListView):
    queryset = Credential.objects.annotate(Count("assignments"))
    table = CredentialTable
    filterset = CredentialFilterSet
    filterset_form = CredentialFilterForm


class CredentialView(generic.ObjectView):
    queryset = Credential.objects.all()

    def get_extra_context(self, request, instance):
        assignments = (
            DeviceCredential.objects.filter(credential=instance)
            .select_related("device")
        )
        table = DeviceCredentialTable(assignments)
        table.configure(request)
        return {"assignments_table": table}


class CredentialEditView(generic.ObjectEditView):
    queryset = Credential.objects.all()
    form = CredentialForm


class CredentialDeleteView(generic.ObjectDeleteView):
    queryset = Credential.objects.all()


# ── DeviceCredential views ──────────────────────────────────────────────────


class DeviceCredentialListView(generic.ObjectListView):
    queryset = DeviceCredential.objects.select_related("credential", "device")
    table = DeviceCredentialTable
    filterset = DeviceCredentialFilterSet
    filterset_form = DeviceCredentialFilterForm


class DeviceCredentialView(generic.ObjectView):
    queryset = DeviceCredential.objects.select_related("credential", "device")


class DeviceCredentialEditView(generic.ObjectEditView):
    queryset = DeviceCredential.objects.all()
    form = DeviceCredentialForm


class DeviceCredentialDeleteView(generic.ObjectDeleteView):
    queryset = DeviceCredential.objects.all()


# ── Bulk-assign view ────────────────────────────────────────────────────────


class BulkAssignView(generic.ObjectEditView):
    """Assign one credential to many devices in a single action."""

    queryset = DeviceCredential.objects.none()  # not used directly
    form = BulkAssignForm
    template_name = "netbox_credentials/bulk_assign.html"

    def get(self, request):
        form = BulkAssignForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = BulkAssignForm(request.POST)
        if form.is_valid():
            credential = form.cleaned_data["credential"]
            devices = form.cleaned_data["devices"]
            role = form.cleaned_data.get("role", "")
            created = 0
            for device in devices:
                _, was_created = DeviceCredential.objects.get_or_create(
                    credential=credential,
                    device=device,
                    role=role,
                )
                if was_created:
                    created += 1
            messages.success(
                request,
                f"Assigned '{credential.name}' to {created} device(s).",
            )
            return redirect("plugins:netbox_credentials:credential_list")
        return render(request, self.template_name, {"form": form})
