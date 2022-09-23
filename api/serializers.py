from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

class TagsSerializerMini(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())

    class Meta:
        model = Tags
        fields = ('name', 'created_by')
        extra_kwargs = {
            'created_by': {'write_only': True},
            'name': {'validators': []},
        }

    def create(self, validated_data):
        tag, created = Tags.objects.get_or_create(**validated_data)
        if not created:
            raise exceptions.ValidationError(validated_data['name']+" already exists.")
        return tag

    def to_representation(self, instance):
        ret = super(TagsSerializerMini, self).to_representation(instance)
        data = dict()
        data['name'] = ret['name']
        return data


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    update_tags = serializers.ListField(
        child=serializers.CharField(max_length=30), write_only=True)

    class Meta:
        model = Posts
        exclude = ()

    def create(self, validated_data):
        tag_names = validated_data.pop('update_tags')
        instance = super().create(validated_data)
        user = self.context['request'].user
        tags = []
        for name in tag_names:
            tag, created = Tags.objects.get_or_create(name=name, defaults={'created_by': user})
            tags.append(tag)
        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('update_tags')
        instance = super().update(instance, validated_data)
        user = self.context['request'].user
        tags = []
        for name in tag_names:
            tag, created = Tags.objects.get_or_create(name=name, defaults={'created_by': user})
            tags.append(tag)
        instance.tags.set(tags)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
