from netbox.plugins import PluginTemplateExtension
from .models import DeviceCredential, PluginSetting


class DeviceCredentialsPanel(PluginTemplateExtension):
    model = "dcim.device"

    def _render_panel(self):
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

    def _get_position(self):
        try:
            return PluginSetting.get().panel_position
        except Exception:
            return "left_page"

    def left_page(self):
        return self._render_panel() if self._get_position() == "left_page" else ""

    def right_page(self):
        return self._render_panel() if self._get_position() == "right_page" else ""

    def full_width_page(self):
        return self._render_panel() if self._get_position() == "full_width_page" else ""


template_extensions = [DeviceCredentialsPanel]
