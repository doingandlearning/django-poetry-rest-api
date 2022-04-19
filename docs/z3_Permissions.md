# Permissions

Security is an important part of any website but it is doubly important with web APIs. 

At the moment, there is no restriction on who can create what on our API - not great!

Django has several out-of-the-box settings we can use.

## Project-Level Permissions

Django Rest Framework config settings are all namespaced inside the REST_FRAMEWORK setting in `settings.py`.

1. Explicitly set the AllowAny setting by adding the following to `settings.py`.

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # new
    ],
}
```

There are four build-in project-level permissions settings:

- AllowAny
- IsAuthenticated
- IsAdminUser
- IsAuthenticatedOrReadOnly

2. Switch to IsAuthenticated.

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # new
    ],
}
```

3. Navigate to your API. If you've logged into the admin panel, you mightn't notice any difference apart from the little `admin` on the top right. Otherwise, you should get 403 Forbidden error.

4. Add a new user in the admin panel.

5. Use your API client and Basic auth to fetch your data.

6. If you want to be able to use the frontend, you can add login/logout pages. In your `urls.py` just add:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("posts.urls")),
    path("api-auth/", include("rest_framework.urls")),  # new
]
```

You should now be able to login and logout.

7. Try changing to `IsAdminUser` which should allow your admin user to get the data but not your test user.

8. Finally, try `IsAuthenticatedOrReadOnly` which should allow you to see the data if you're not logged in but update it if you are.


## View-Level Permissions

If you're using generics, you can add `permission_classes` easily to your views.

```python
class BookDetail(generics.RetrieveUpdateDestroyAPIView): 
	permission_classes = (permissions.IsAdminUser,) # new 
	queryset = Book.objects.all()
  serializer_class = BookSerializer
```

Now, only the admin can see the detail, authenicated users can see and update on the list and unauthenicated users can only see the list.

## Custom Permissions

All custom permissions override this base class.

```python
class BasePermission(object): 
	"""
  A base class from which all permission classes should inherit.
  """
	def has_permission(self, request, view): 
	"""
	Return `True` if permission is granted, `False` otherwise. 
	"""
	return True

	def has_object_permission(self, request, view, obj): 
	"""
  Return `True` if permission is granted, `False` otherwise.
	"""
	return True
```

You can add more nuance depending on how your want to secure.

Here's a permission that will only allow the author to update something.

```python

class IsAuthorOrReadOnly(permissions.BasePermission): 
	def has_permission(self, request, view):
    # Authenticated users only can see list view
		if request.user.is_authenticated: 
			return True
		return False
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request so we'll always 
		# allow GET, HEAD, or OPTIONS requests
		if request.method in permissions.SAFE_METHODS:
			return True
    # Write permissions are only allowed to the author of a post
		return obj.author == request.user
```

We'd then add this class in our views to the `permission_classes`.