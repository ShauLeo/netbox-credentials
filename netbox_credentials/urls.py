from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import views
from .models import Credential, DeviceCredential

urlpatterns = [
    # ── Credentials ─────────────────────────────────────────────────
    path("credentials/", views.CredentialListView.as_view(), name="credential_list"),
    path("credentials/add/", views.CredentialEditView.as_view(), name="credential_add"),
    path("credentials/<int:pk>/", views.CredentialView.as_view(), name="credential"),
    path("credentials/<int:pk>/edit/", views.CredentialEditView.as_view(), name="credential_edit"),
    path("credentials/<int:pk>/delete/", views.CredentialDeleteView.as_view(), name="credential_delete"),
    path("credentials/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="credential_changelog", kwargs={"model": Credential}),

    # ── Device Credential Assignments ───────────────────────────────
    path("assignments/", views.DeviceCredentialListView.as_view(), name="devicecredential_list"),
    path("assignments/add/", views.DeviceCredentialEditView.as_view(), name="devicecredential_add"),
    path("assignments/<int:pk>/", views.DeviceCredentialView.as_view(), name="devicecredential"),
    path("assignments/<int:pk>/edit/", views.DeviceCredentialEditView.as_view(), name="devicecredential_edit"),
    path("assignments/<int:pk>/delete/", views.DeviceCredentialDeleteView.as_view(), name="devicecredential_delete"),
    path("assignments/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="devicecredential_changelog", kwargs={"model": DeviceCredential}),

    # ── Bulk assign ─────────────────────────────────────────────────
    path("bulk-assign/", views.BulkAssignView.as_view(), name="bulk_assign"),
]
