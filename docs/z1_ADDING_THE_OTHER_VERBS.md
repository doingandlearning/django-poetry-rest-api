# CRUD

So far, you've looked at adding a List all and a ListDetail view - the "R" of our CRUD API.

CRUD stands for:

Create
Read
Update
Delete

which is the bread and butter of every web API!

Let's work on adding the other 3 letters today.

# Create

We want to be able to create a new resource. The verb involved here is POST. 

1. Extend your list view and add a `post` method. This code snippet uses books and book serializer, adapt it to your use case.

```python
def post(self, request, format=None):
		serializer = BookSerializer(data=request.data)
		if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

2. Going to your API route `http://localhost:8000/books` for example, there should now be a form at the bottom to allow you to POST a new record. Do this here.

3. Test that you can use your API client to do this as well (Postman/Insomnia/Paw/etc).

# Read

We've already handled this one. But check the list view has all of your records and that you can view individual records.

# Update

There is some arguments between developers over PUT or PATCH for an update. Both are valid so be aware that for update, you may see either verb used.

It only makes sense to update a particular resource, so we're going to update the detail view.

1. Extend your detail view to add the `put` method below. Again, update to reflect your model.

```python
def put(self, request, pk, format=None):
		book = self.get_object(pk)
		serializer = BookSerializer(book, data=request.data)
		if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

2. Going to your API route `http://localhost:8000/books/1` for example, there should now be a form at the bottom to allow you to PUT and update your record. Do this here.

3. Test that you can use your API client to do this as well (Postman/Insomnia/Paw/etc). 

# Delete

Finally, our delete function. Again, this only makes sense for a particular record and, again, you'll need to update your code to reflect your particular model.

1. Extend your detail view to add the `delete` method below. Again, update to reflect your model.

```python
def delete(self, request, pk, format=None):
		book = self.get_object(pk)
		book.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
```

2. Going to your API route `http://localhost:8000/books/1` for example, there should now be a DELETE button at the top to allow you to delete your record. Do this here.

3. Test that you can use your API client to do this as well (Postman/Insomnia/Paw/etc) - though you'll need to use a different record.


# Refactor with mixins

Writing out the same code for every verb is frustrating and verbose. The joys of working in an object oriented way is that we can inherit from other classes.

A mixin is an abstract class - one that doesn't exist on it's own but that other classes can inherit from. This allows for properties and methods to be bundled and shared.

We can refactor our ListView to use mixins like this.

```python
class BookList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

We have to add two new class properties - the `queryset` and the `serializer_class`. 

We still have to define the verbs but all of the logic is handled by the mixins. 

The detail looks very similar.

```python
class BookDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

Refactor your application to use mixins. Retest to make sure you can do all of the operations from your application.



# Refactor to Generic Views

> Django’s generic views... were developed as a shortcut for common usage patterns... They take certain common idioms and patterns found in view development and abstract them so that you can quickly write common views of data without having to repeat yourself. - [Django Documentation](https://docs.djangoproject.com/en/4.0/ref/class-based-views/#base-vs-generic-views)

The DRF provides some generic views for the [most common API use cases](https://www.django-rest-framework.org/api-guide/generic-views/).


To refactor now, we just change what we are inheriting from and remove our custom method code.

```python
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

