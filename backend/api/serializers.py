import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from api.models import Amount, Ingredient, Recipe, Tag
from users.serializers import UserListOrDetailSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения тэгов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиетов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class AmountSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиентов при отображении рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(
        source='ingredient')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    """Сериализатор поля картинок."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта
    при получении списка рецептов и конкретного рецепта."""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = AmountSerializer(many=True, source='recipe')
    author = UserListOrDetailSerializer()
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
            )


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных
    рецепта при создании и обновлении."""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = AmountSerializer(many=True, source='recipe')

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time"
            )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор получаемых ингредиентов
    при создании и обновлении рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Amount  # Intermediate model
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта при создании и обновлении."""
    image = Base64ImageField(required=True, allow_null=False)
    author = UserListOrDetailSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть мнинмум 1 минута!')
        return cooking_time

    def validate_ingredients(self, ingredients):
        if len(ingredients) < 1:
            raise serializers.ValidationError(
                'Должен присутствовать минимум один ингредиент')
        list_of_ingredients = []
        for current_item in ingredients:
            if current_item['ingredient'] in list_of_ingredients:
                raise serializers.ValidationError(
                    ('Ингредиент в рецепте должен'
                     ' встречаться не более одного раза.'))
            list_of_ingredients.append(current_item['ingredient'])
        return ingredients

    def create_ingredients(self, ingredients, recipe):
        """Создание списка ингредиентов с количествами"""
        for current_ingredient in ingredients:
            Amount.objects.create(
                recipe=recipe,
                ingredient=current_ingredient['ingredient'],
                amount=current_ingredient['amount']
                )

    def update(self, recipe, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.create_ingredients(ingredients, recipe)
        if 'tags' in validated_data:
            recipe.tags.set(
                validated_data.pop('tags'))
        return super().update(
            recipe, validated_data)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe: Recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Класс для отображения рецепта при добавлении в Избранное или Корзину"""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
