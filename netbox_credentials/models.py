from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from dcim.models import Device

from .crypto import encrypt, decrypt


class Credential(NetBoxModel):
    """
    A reusable credential object.  Create it once (e.g. "default-pw") and
    assign it to as many devices as you like.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Friendly name, e.g. 'default-pw' or 'snmp-ro-community'",
    )
    username = models.CharField(
        max_length=200,
        blank=True,
        default="",
    )
    _password = models.TextField(
        db_column="password",
        blank=True,
        default="",
        verbose_name="Password (encrypted)",
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )
    comments = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Credential"
        verbose_name_plural = "Credentials"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_credentials:credential", args=[self.pk])

    # ── password property (encrypt on write, decrypt on read) ──

    @property
    def password(self) -> str:
        return decrypt(self._password) if self._password else ""

    @password.setter
    def password(self, value: str):
        self._password = encrypt(value) if value else ""

    # convenience for templates
    @property
    def password_is_set(self) -> bool:
        return bool(self._password)


class DeviceCredential(NetBoxModel):
    """
    Links a Credential to a Device.
    Optional ``role`` field lets you distinguish e.g. "management" vs "snmp".
    """

    credential = models.ForeignKey(
        to=Credential,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name="credential_assignments",
    )
    role = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Optional role, e.g. 'management', 'snmp', 'api'",
    )

    class Meta:
        ordering = ["credential__name"]
        unique_together = ("credential", "device", "role")
        verbose_name = "Device Credential Assignment"
        verbose_name_plural = "Device Credential Assignments"

    def __str__(self):
        role_str = f" ({self.role})" if self.role else ""
        return f"{self.credential.name} → {self.device}{role_str}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_credentials:devicecredential", args=[self.pk])
