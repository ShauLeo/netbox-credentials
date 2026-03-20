from netbox.plugins import PluginTemplateExtension

from .models import DeviceCredential
from .tables import DeviceCredentialTable


class DeviceCredentialsPanel(PluginTemplateExtension):
    """Inject a credentials panel into the Device detail page."""

    model = "dcim.device"

    def full_width_page(self):
        device = self.context["object"]
        request = self.context["request"]
        assignments = (
            DeviceCredential.objects.filter(device=device)
            .select_related("credential")
        )

        if not assignments.exists():
            return ""

        table = DeviceCredentialTable(assignments)
        table.configure(request)

        return self.render(
            "netbox_credentials/inc/device_credentials_panel.html",
            extra_context={"assignments_table": table},
        )


template_extensions = [DeviceCredentialsPanel]
