from rest_framework import generics
from .models import VcMV, VcCL, VcDNS
from .serializers import VideoCardsSerializer


class VcMVListView(generics.ListAPIView):
    queryset = VcMV.objects.all()
    serializer_class = VideoCardsSerializer


class VcDNSListView(generics.ListAPIView):
    queryset = VcDNS.objects.all()
    serializer_class = VideoCardsSerializer


class VcCLListView(generics.ListAPIView):
    queryset = VcCL.objects.all()
    serializer_class = VideoCardsSerializer
