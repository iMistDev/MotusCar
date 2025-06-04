from rest_framework import viewsets
from .models import Valoracion
from .serializers import ValoracionSerializer
from rest_framework.permissions import IsAuthenticated

class ValoracionViewSet(viewsets.ModelViewSet):
    queryset = Valoracion.objects.all()
    serializer_class = ValoracionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
