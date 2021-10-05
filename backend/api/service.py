import operator

from rest_framework import serializers


def calc_cpc(data: dict):
    """
    Calculates a cpc (cost per click) by formula cost/clicks.
    :param data: dict with cost and clicks data.
    :return: cpc or raises validation error.
    """
    try:
        cost = data['cost']
        clicks = data['clicks']
        if clicks:
            return float(cost) / int(clicks)
        else:
            return 0
    except KeyError:
        raise serializers.ValidationError('Unable to calculate cpc')


def calc_cpm(data: dict):
    """
    Calculates a cpm (cost of 1000 impressions) by formula cost/views*1000.
    :param data: dict with cost and views data.
    :return: cpm or raises validation error.
    """
    try:
        cost = data['cost']
        views = data['views']
        if views:
            return float(cost) / int(views) * 1000
        else:
            return 0
    except KeyError:
        raise serializers.ValidationError('Unable to calculate cpm')


def sort_response(response, request):
    """
    Sorts response by url param (ordering).
    :return: sorted response.
    """
    ordering = request.query_params.get('ordering')
    if ordering:
        response.data = sort_dict(response.data, ordering=ordering)

    return response


def sort_dict(data, ordering: str):
    """
    Adds functionality to recognize symbol "-" before ordering field.
    :param data: data to sort.
    :param ordering: field of data.
    :return: sorted data.
    """
    if "-" in ordering:
        ordering = ordering[1:]
        data = sorted(
            data,
            key=get_key_func(ordering),
            reverse=True
        )
    else:
        data = sorted(
            data,
            key=get_key_func(ordering)
        )
    return data


def get_key_func(ordering: str):
    """
    Gets sort key function. Depends on ordering field.
    :param ordering: field of data.
    :return: sort key function.
    """
    if ordering == "cost":
        # It's configured this way cause now it will sort as a float, not a str.
        key_func = lambda k: (float(k[ordering]),)
    else:
        key_func = operator.itemgetter(ordering)
    return key_func
