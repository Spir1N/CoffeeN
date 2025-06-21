from django import template

register = template.Library()

@register.simple_tag
def star_class(avg_rating: float, position: int) -> str:
    """
    Возвращает CSS‑класс для i‑иконки Bootstrap:
    - bi-star-fill  (полная)
    - bi-star-half  (половинка)
    - bi-star       (пустая)
    """
    try:
        avg = float(avg_rating)
    except (TypeError, ValueError):
        avg = 0.0

    if position <= int(avg):
        return "bi-star-fill"
    if position - 0.5 <= avg:
        return "bi-star-half"
    return "bi-star"
