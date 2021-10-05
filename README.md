#  Microservice_REST

## Stack: ##

- **Django**
  - restframework
- Docker
- PostgreSQL

## Usage: ##

  ```sh
  git clone git@github.com:DanilTka/microservice_REST.git

  cd microservice_REST
  
  docker-compose up --build
  ```
## Use example: ##
http://127.0.0.1:8000/?from=2018-01-01&to=2021-05-10&ordering=-date
1. Sort output date any field (ordering). 
2. Select query in date range with params (from, to).
3. Provides methods only to an admin user.

**Preloaded admin:**

- *username: admin*
- *password: admin*

## Methods: ##

Provides appropriate queryset from url params:
 ```python
    def get_queryset(self):
        """
        Gets queryset in the date range if url has params (from, to) if not returns all objects.
        Sort result queryset by date.
        :return: sorted by date queryset.
        """
        if self.request.query_params.get("from") and self.request.query_params.get("to"):
            from_ = self.request.query_params['from']
            to_ = self.request.query_params['to']
            queryset = Statistics.objects.filter(
                date__range=[from_, to_]
            ).order_by('-date')
        else:
            queryset = Statistics.objects.all().order_by('-date')
        return queryset
```
Expand list to add sort:
```python
class Statistics_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = Statistics_serializer
    ordering_fields = ['date', 'views', 'clicks', 'cost', 'cpc', 'cpm']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if self.request.query_params.get("ordering"):
            return sort_response(response, request)
        else:
            return response
```
Delete realization:
```python
def destroy(self, request, *args, **kwargs):
    Statistics.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```
Cpc and cpm calculation:
```python
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
```
Usage. Add new data to serializer:
```python
def save(self, **kwargs):
    """
    Before saving, it calculates CPC, CPM then, adding them to validated_data.
    :param kwargs:
    :return:
    """
    self.validated_data['cpc'] = calc_cpc(self.validated_data)
    self.validated_data['cpm'] = calc_cpm(self.validated_data)
    return super(Statistics_serializer, self).save()
```
ModelSerializer with date field additional validation:
```python
class Statistics_serializer(serializers.ModelSerializer):
    cpc = serializers.ReadOnlyField()
    cpm = serializers.ReadOnlyField()

    def validate_date(self, date_):
        """
        Checks if date >= 2000-01-01 and <= today's date.
        :param date_: input date. format(YYYY-MM-DD).
        :return: date or validation error.
        """
        min_date = date(2000, 1, 1)
        max_date = date.today()
        if date_ <= min_date or date_ >= max_date:
            raise serializers.ValidationError('The date has to be >= 2000-01-01 and <= today')
        else:
            return date_
```
To sort response data by any field functions was added:
```python
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
```
The function that separates the "cost" field and gives another key function. It needs to sort costs as python float.
```python
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
```
