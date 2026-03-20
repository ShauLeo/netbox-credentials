from netbox.plugins import PluginTemplateExtension
from .models import DeviceCredential

class DeviceCredentialsPanel(PluginTemplateExtension):
    model = "dcim.device"

    def right_page(self):
        device = self.context["object"]
        assignments = (
            DeviceCredential.objects.filter(device=device)
            .select_related("credential")
        )
        if not assignments.exists():
            return ""
        return self.render(
            "netbox_credentials/inc/device_credentials_panel.html",
            extra_context={"assignments": assignments},
        )

template_extensions = [DeviceCredentialsPanel]
