from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from users.permissions import HasUserProfile, IsAdminManagerOrSeller, IsAdminOrManager, IsSameFranchise
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, HasUserProfile, IsAdminManagerOrSeller, IsSameFranchise]

    def get_permissions(self):
        if self.action in {"destroy"}:
            return [IsAuthenticated(), HasUserProfile(), IsAdminOrManager()]
        return [IsAuthenticated(), HasUserProfile(), IsAdminManagerOrSeller()]

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = Customer.objects.filter(franchise=profile.franchise)
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(document__icontains=query))
        return queryset

    def perform_create(self, serializer):
        serializer.save(franchise=self.request.user.profile.franchise)
