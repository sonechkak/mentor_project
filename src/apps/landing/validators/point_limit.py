from django.core.exceptions import ValidationError


def max_seven_points_for_product(product):
    """ Валидатор, который проверяет, что для данного продукта не создано более 7 пунктов. """
    from apps.landing.models import Point
    count = Point.objects.filter(product=product).count()
    if count >= 7:
        raise ValidationError("Не допускается создание более 7 пунктов для этого продукта.")