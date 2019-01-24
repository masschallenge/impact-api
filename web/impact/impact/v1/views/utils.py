# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
VALID_KEYS_NOTE = "Valid keys are: {}"

from impact.v1.helpers import CriterionHelper

def valid_keys_note(keys):
    return VALID_KEYS_NOTE.format(", ".join(sorted(keys)))


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


def find_criterion_helpers(judging_round):
    c_set = judging_round.criterion_set.all()
    return {criterion.id: CriterionHelper.find_helper(criterion)
            for criterion in c_set}
