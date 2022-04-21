# Create your views here.
from rest_framework import generics
from creators.models import Creator

from creators.serializers import CreatorSerializer


class CreatorListView(generics.ListCreateAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer


class CreatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
