from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import login
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views

from .serializers import *
from .models import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


class UserSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password',
                  'first_name',
                  'last_name',
                  'password')
        read_only_fields = ('date_created', 'date_modified', 'username')

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None,{
        "username": UserSerializer(user, context=self.get_serializer_context()).data,
        "password": AuthToken.objects.create(user)[1]
        },status=status.HTTP_202_ACCEPTED)

class PostViewset(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Posts.objects.all()
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [AllowAny]
	filter_backends = [DjangoFilterBackend]
	ordering_fields = 'created_by'
	search_fields = ['created_by','id']
	filterset_fields = {
		'id':['exact'],
	}

	@api_view(['GET', 'POST', 'DELETE'])
	def post_list(request):
		if request.method == 'GET':
			posts = Post.objects.all()

			title = request.query_params.get('title', None)

			if title is not None:
				posts = posts.filter(title__icontains=title)
				posts_serializer = PostSerializer(posts, many=True)
			return JsonResponse(posts_serializer.data, safe=False)

		elif request.method == 'POST':
			post_data = JSONParser().parse(request)
			posts_serializer = PostSerializer(data=post_data)
			if posts_serializer.is_valid():
				posts_serializer.save()
				return JsonResponse(posts_serializer.data, status=status.HTTP_201_CREATED)
			return JsonResponse(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			count = Post.objects.all().delete()
			return JsonResponse({'message': '{} Posts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
class CommentViewset(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	permission_classes = [AllowAny]

class TagsViewset(viewsets.ModelViewSet):
	serializer_class = TagsSerializerMini
	queryset = Tags.objects.all()
	permission_classes = [AllowAny]


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
    	serializer = self.serializer_class(request.user, data=request.data, partial=True)
    	serializer.is_valid(raise_exception=True)
    	serializer.save()
    	return Response(serializer.data, status=status.HTTP_200_OK)


