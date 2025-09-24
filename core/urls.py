from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, PacienteViewSet, MedicamentoViewSet, PrescricaoViewSet, AdministracaoViewSet, AlertaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'prescricoes', PrescricaoViewSet)
router.register(r'administracoes', AdministracaoViewSet)
router.register(r'alertas', AlertaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include('core.urls_frontend')),
]

