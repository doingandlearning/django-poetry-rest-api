from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Show
from .serializers import ShowSerializer


# CRUD
# Create -> POST ✅
# Read -> GET ✅
# Update -> PUT/PATCH ✅
# Delete -> DELETE✅


class ShowListView(APIView):
    # `_request` is not used. The leading underscore expresses that it won't be used.
    # /shows
    def get(self, _request):
        shows = Show.objects.all()
        serialized_shows = ShowSerializer(shows, many=True)
        return Response(serialized_shows.data)

    def post(self, request):
        serialized_show = ShowSerializer(data=request.data)
        if serialized_show.is_valid():
            serialized_show.save()
            return Response(serialized_show.data, status=status.HTTP_201_CREATED)
        return Response(serialized_show.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowDetailView(APIView):
    def get_object(self, pk):
        try:
            return Show.objects.get(id=pk)
        except:
            raise Http404()

    def get(self, _request, pk):
        show = self.get_object(pk)  # Where is the pk coming from??
        serialized_show = ShowSerializer(show, many=False)
        return Response(serialized_show.data)

    def put(self, request, pk):
        show = self.get_object(pk)
        serialized_show = ShowSerializer(show, data=request.data)

        if serialized_show.is_valid():
            serialized_show.save()
            return Response(serialized_show.data, status=status.HTTP_200_OK)

        return Response(serialized_show.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _request, pk):
        show = self.get_object(pk)
        show.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
