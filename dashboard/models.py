# dashboard/models.py

from django.db import models

# Creamos un modelo simple solo para poder asociarle permisos personalizados.
class DashboardModel(models.Model):

    class Meta:
        # La sección 'permissions' nos permite definir permisos adicionales.
        permissions = [
            ("index_viewer", "Can show to index view (function-based)"),
        ]