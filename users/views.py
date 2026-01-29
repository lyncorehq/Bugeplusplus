from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Seller
from .permissions import HasUserProfile, IsAdminOrManager, IsSameFranchise
from .serializers import MeSerializer, SellerSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated, HasUserProfile]

    def get(self, request):
        return Response(MeSerializer(request.user).data)

class SellerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasUserProfile, IsAdminOrManager, IsSameFranchise]
    serializer_class = SellerSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return Seller.objects.filter(franchise=profile.franchise).select_related("user")
