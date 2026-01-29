from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Seller
from .permissions import HasUserProfile, IsAdminOrManager, IsSameFranchise
from .serializers import MeSerializer, SellerCreateSerializer, SellerSerializer, SellerUpdateSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated, HasUserProfile]

    def get(self, request):
        return Response(MeSerializer(request.user).data)

class SellerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasUserProfile, IsAdminOrManager, IsSameFranchise]
    serializer_class = SellerSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return SellerCreateSerializer
        if self.action in {"update", "partial_update"}:
            return SellerUpdateSerializer
        return SellerSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return Seller.objects.filter(franchise=profile.franchise).select_related("user")

    def perform_create(self, serializer):
        serializer.save(franchise=self.request.user.profile.franchise)
