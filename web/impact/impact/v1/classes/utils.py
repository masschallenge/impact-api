def collect_pairs(pairs):
    result = {}
    for first, second in pairs:
        value = result.get(first)
        if value:
            value.append(second)
        else:
            result[first] = [second]
    return result
