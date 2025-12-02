from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet,
    PacienteViewSet,
    MedicamentoViewSet,
    PrescricaoViewSet,
    AdministracaoViewSet,
    AlertaViewSet,
    AlertasPendentesAPIView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'prescricoes', PrescricaoViewSet)
router.register(r'administracoes', AdministracaoViewSet)
router.register(r'alertas', AlertaViewSet)

urlpatterns = [
    # endpoint custom de alertas pendentes
    path('api/alertas/pendentes/', AlertasPendentesAPIView.as_view(), name='alertas_pendentes_api'),

    # demais endpoints REST (ViewSets)
    path('api/', include(router.urls)),

    # frontend HTML
    path('', include('core.urls_frontend')),
]
