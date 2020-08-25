from apps.food_quantity.models import FoodQuantity


def is_none(parm):
    """
    参数parm是不是 None，是就返回 '—'
    :param backfat:
    :return:
    """
    return parm if parm is not None else '—'
