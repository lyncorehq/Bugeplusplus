from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import HasUserProfile, IsAdminManagerOrSeller, IsSameFranchise
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, HasUserProfile, IsAdminManagerOrSeller, IsSameFranchise]

    def get_queryset(self):
        profile = self.request.user.profile
        return Customer.objects.filter(franchise=profile.franchise)

    def perform_create(self, serializer):
        serializer.save(franchise=self.request.user.profile.franchise)
