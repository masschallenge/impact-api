def merge_data_by_id(data):
    result = {}
    for datum in data:
        id = datum["id"]
        item = result.get(id, {})
        item.update(datum)
        result[id] = item
    return result.values()


def map_data(klass, query, order, data_keys, output_keys):
    result = klass.objects.filter(query).order_by(order)
    data = result.values_list(*data_keys)
    return [dict(zip(output_keys, values))
            for values in data]
