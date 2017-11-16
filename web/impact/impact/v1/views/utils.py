# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


def coalesce_dictionaries(data, merge_field="id"):
    """Takes a sequence of dictionaries, merges those that share the
    same merge_field, and returns a list of resulting dictionaries"""
    result = {}
    for datum in data:
        merge_id = datum[merge_field]
        item = result.get(merge_id, {})
        item.update(datum)
        result[merge_id] = item
    return result.values()


def map_data(klass, query, order, data_keys, output_keys):
    result = klass.objects.filter(query).order_by(order)
    data = result.values_list(*data_keys)
    return [dict(zip(output_keys, values))
            for values in data]
