from rest_framework import permissions, generics
from coupon.models import Coupon
from coupon.api.serializers import CouponSerializer

# Create your views here.
class CouponAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer