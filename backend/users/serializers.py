from api.models import Recipe
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserListOrDetailSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=author).exists()


class RecipeForSubsciptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time")


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    recipes = RecipeForSubsciptionsSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, user):
        return user.recipes.all().count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = (
            obj.author.recipe.all()[:int(limit)] if limit
            else obj.author.recipe.all())
        return RecipeForSubsciptionsSerializer(
            recipes,
            many=True).data

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        return user.follower.filter(author=author).exists()
