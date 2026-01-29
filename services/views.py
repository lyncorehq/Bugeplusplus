from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import HasUserProfile, IsAdminOrManager, IsSameFranchise
from .models import Plan
from .serializers import PlanSerializer


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated, HasUserProfile, IsSameFranchise]

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [IsAuthenticated(), HasUserProfile()]
        return [IsAuthenticated(), HasUserProfile(), IsAdminOrManager()]

    def get_queryset(self):
        profile = self.request.user.profile
        return Plan.objects.filter(franchise=profile.franchise)

    def perform_create(self, serializer):
        serializer.save(franchise=self.request.user.profile.franchise)
