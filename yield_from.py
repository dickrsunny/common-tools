from collections import namedtuple

# pylint: disable=E1101, E1111


Result = namedtuple('Result', 'count average')


# the subgenerator
def averager():  # <1>
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  # <2>
        if term is None:  # <3>
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # <4>


# the delegating generator
def grouper(results, key):  # <5>
        _i = averager()  # <1>
        try:
            _y = next(_i)  # <2>
        except StopIteration as _e:
            _r = _e.value  # <3>
        else:
            while 1:  # <4>
                _s = yield _y  # <5>
                try:
                    _y = _i.send(_s)  # <6>
                except StopIteration as _e:  # <7>
                    _r = _e.value
                    break

        results[key] = _r

        # results[key] = yield from averager()   # 上面方法与此行等效


# the client code, a.k.a. the caller
def main(data):  # <8>
    results = {}
    for key, values in data.items():
        group = grouper(results, key)  # <9>
        next(group)  # <10>
        for value in values:
            group.send(value)  # <11>
        try:
            group.send(None)  # important! <12>
        except StopIteration:
            pass

    # print(results)  # uncomment to debug
    report(results)


# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
              result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
    main(data)
