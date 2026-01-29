from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import HasUserProfile, IsAdminManagerOrSeller, IsSameFranchise
from .models import Contract
from .serializers import ContractSerializer, ContractStateSerializer


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, HasUserProfile, IsAdminManagerOrSeller, IsSameFranchise]

    def get_queryset(self):
        profile = self.request.user.profile
        return (
            Contract.objects.filter(franchise=profile.franchise)
            .select_related("customer", "plan")
        )

    def perform_create(self, serializer):
        serializer.save(franchise=self.request.user.profile.franchise)

    @action(detail=True, methods=["patch"], url_path="state")
    def set_state(self, request, pk=None):
        contract = self.get_object()
        serializer = ContractStateSerializer(contract, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ContractSerializer(contract).data)
