# Related Data

Often our data will be related in different ways. Rather than storing everything in one model, we'll want to store and retrieve them seperately. 

## Set up your related app

For me, I'm going to add an actor app to store data about the actors I care about. I'm going to start with the star of each show.

1. Add a new app, here's the command for the actors app: `python manage.py startapp actors`

2. In your new app add a model to describe the data.

3. Add your new app to the `settings.py` in the main app.

4. Make and apply your migrations. `python manage.py makemigrations` and `python manage.py migrate`.

You can decide if you want to be able to have a full CRUD for this particular model or just update in the admin.

### Full CRUD

We'll need to add the serializers, the views and the urls to our new app. We'll then need to add the urls to our main app.

1. Create a new `serializers.py` and adapt the serializer for your model:

```python
from rest_framework import serializers

from .models import Show

class ShowSerializer(serializers.ModelSerializer):
    """ Serializer of a show """

    class Meta:
        model = Show
        fields = '__all__'
```

2. Use the generics to add the views - again, adapt to your model.

```python
from django.shortcuts import render

from rest_framework import generics

from actors.models import Actor
from actors.serializers import ActorSerializer

class ActorListView(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class ActorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
```

3. Create a `urls.py` in your new app and add your urls (... adapt):

```python
from django.urls import path
from .views import ActorListView, ActorDetailView

urlpatterns = [
    path('', ActorListView.as_view()),
    # with `<str:pk>` we store whatever is part of the url at that position in a variable called 'pk'
    path('<str:pk>/', ActorDetailView.as_view())
]
```

4. In the main app, update your urls to capture your new apps urls:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shows/', include('shows.urls')),
    path('actors/', include('actors.urls')),
]
```

### Create through Admin

We're not going to look at updating the Django admin, so you won't be able to do some of the reverse lookup things we'll explore later if you take this approach.

1. Register your model in the `admin.py` of your new app.


## Adding a related field

1. In your original app, you need to import the model and declare a new relationship:

```python
    star = models.ForeignKey(Actor,
                             on_delete=models.CASCADE, null=True)
```																											

2. Now you'll need to make and apply your migrations. 

3. If you view in the Django admin, you'll be able to select your related field. (If you haven't already you might want to update the `__str__` of your new related model)

## Adding a Many-To-Many field

1. Add in the new property with the Many-To-Many relationship.

```python
    supporting_actors = models.ManyToManyField(Actor)
```

2. Now you'll need to make and apply your migrations. 

3. If you view in the Django admin, you'll be able to select multiple options of your related field. (If you haven't already you might want to update the `__str__` of your new related model).

## Reading from related fields

By default, our related fields will give us the primary keys of their partner. 

If it is a foreign key relationship, a blank field will be null and won't appear on our API output. 

If it is a many-to-many relationship, a blank field will give us an empty list.

To change how the API responds, we have a number of options. We can use one of the built in serializers or create one of our own.

By default, this is being displayed as a PrimaryKeyRelatedField with read_only set to True.

```python
    star = serializers.PrimaryKeyRelatedField(read_only=True)
```

### StringRelatedField

The first way you can change this is with StringRelatedField, this will use the `__str__` method to respond.

```python
    star = serializers.StringRelatedField()
```

### SlugRelatedField

The next is to use any field as a slug:

```python
    star = serializers.SlugRelatedField(
        slug_field="first_name", read_only=True)
```

### HyperlinkRelatedField

You can provide a hyperlink connection to the related field. This fits with the REST definition really well.

1. Make sure you have named the detail view in your urls:

```python
urlpatterns = [
    path('', ActorListView.as_view()),
    # with `<str:pk>` we store whatever is part of the url at that position in a variable called 'pk'
    path('<str:pk>/', ActorDetailView.as_view(), name="actor-detail")
]

```

2. Add the HyperlinkedRelatedField as follows:

```python
    supporting_actors = serializers.HyperlinkedRelatedField(
        many=True, view_name="actor-detail", read_only=True)

```

### Custom Serializer

Probably, the most useful is to use a custom serializer.

```python
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'first_name', 'last_name')
```

## Reverse lookup

What about reading data in the opposite direction? For example, which shows did this actor star in?

1. The first thing you'll need to do is add a `related_name` to field in the model.

```python
    star = models.ForeignKey(Actor, related_name="shows",
                             on_delete=models.CASCADE, null=True)

    supporting_actors = models.ManyToManyField(
        Actor, related_name="supported")
```

2. Then you have all the options as above for adapting the serializer.

## Creating records

If we use a nested serializer when _creating_ or _updating_ a record it will expect to receive data in the format that it outputs the data. So if we used a populated serializer when creating a record, it would expect to receive nested data.

This may be desirable, however, you would also need to write logic to describe _how_ the serializer should deal with that data.

Here's an example with the `PopulatedTrackSerializer` above:

```py
class PopulatedTrackSerializer(TrackSerializer):

    artist = ArtistSerializer()
    genres = GenreSerializer(many=True)


    def create(self, data):
        artist_data = data.pop('artist')
        genres_data = data.pop('genres')

        # create an artist without artist or genre data
        track = Track(**data)
        # find the existing artist or create one if not found and add to the newly created track
        track.artist = Artists.get_or_create(**artist_data)
        # find the existing genres or create them if not found
        genres = [Genre.get_or_create(**genre_data) for genre_data in genres_data]
        track.set(genres) # set the genres to the track

        return track # return the completed track


    def update(self, track, data):
        artist_data = data.pop('artist')
        genres_data = data.pop('genres')

        track.name = data.get('name', track.name)
        track.released = data.get('released', track.released)
        track.length = data.get('length', track.length)

        if artist_data:
            track.artist = Artists.get_or_create(**artist_data)

        if genres_data:
            genres = [Genre.get_or_create(**genre_data) for genre_data in genres_data]
            track.set(genres)

        return track

```

This means that data can be sent from the client to the server in the same format that it is sent from server to client.

We would now need to update the view to use this template for creating and updating:

```py
class TrackList(APIView):

    def post(self, request):
        serializer = PopulatedTrackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save() # this will call the `create` method

            return Response(serializer.data, status=201)

        return Response(serializer.data, status=422)
```