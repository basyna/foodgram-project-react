from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга'
        )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой код тэга'
        )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слэг поле (обязательно)'
        )

    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецептов'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
        )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
        )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['id', 'name', ]

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    def add_user_annotations(self, user_id):
        return self.annotate(
            is_favorited=models.Exists(
                Favorite.objects.filter(
                    user=user_id,
                    recipe__pk=models.OuterRef('pk')
                )
            ),
            is_in_shopping_cart=models.Exists(
                ShoppingCart.objects.filter(
                    user__id=user_id,
                    recipe__pk=models.OuterRef('pk')
                )
            )
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
        )
    name = models.CharField(
        'Название рецепта',
        max_length=150,
    )
    image = models.ImageField(
        upload_to='img/',
        null=False,
        blank=False,
        verbose_name='Изображение'
        )
    text = models.TextField(
        'Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
        verbose_name='Ингредиенты'
        )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги'
        )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Время приготовления (мин.)'
        )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество продукта',
        help_text='Введите количество продукта'
        )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количества ингредиентов'

    def __str__(self):
        return f'В "{self.recipe}" входит "{self.ingredient}"'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранный рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return (
            f'Пользователь "{self.user}"'
            f' добавил "{self.recipe}" в Избранные.'
            )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        return f'Пользователь "{self.user}" добавил "{self.recipe}" в покупки.'
