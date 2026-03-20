from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views import View

from netbox.views import generic

from .filtersets import CredentialFilterSet, DeviceCredentialFilterSet
from .forms import (
    BulkAssignForm,
    CredentialFilterForm,
    CredentialForm,
    DeviceCredentialFilterForm,
    DeviceCredentialForm,
    PluginSettingForm,
)
from .models import Credential, DeviceCredential, PluginSetting
from .tables import CredentialTable, DeviceCredentialTable


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


class BulkAssignView(generic.ObjectEditView):
    queryset = DeviceCredential.objects.none()
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
            messages.success(request, f"Assigned '{credential.name}' to {created} device(s).")
            return redirect("plugins:netbox_credentials:credential_list")
        return render(request, self.template_name, {"form": form})


class PluginSettingView(View):
    def get(self, request):
        instance = PluginSetting.get()
        form = PluginSettingForm(instance=instance)
        return render(request, "netbox_credentials/settings.html", {"form": form})

    def post(self, request):
        instance = PluginSetting.get()
        form = PluginSettingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Credentials plugin settings saved.")
            return redirect("plugins:netbox_credentials:settings")
        return render(request, "netbox_credentials/settings.html", {"form": form})
