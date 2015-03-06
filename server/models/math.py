def average(list):
    if list.count() == 0:
        return 0.0
    else:
        return round(sum([x.vote for x in list]) / float(list.count()), 2)


def variance(list):
    if list.count() == 0:
        return 0.0
    else:
        variance_val = 0
        average_val = average(list)
        for i in list:
            variance_val += (average_val - i.vote) ** 2
        return round(variance_val / list.count(), 2)
