import time
import multiprocessing


# multiprocessing
def multiprocessing_evaluation(result, lock, start, end):
    local_sum = 0
    for i in range(start, end + 1):
        local_sum += 1 / i
    with lock:
        result.value += local_sum

# simple Python eval
def simple_evaluation():
    result = 0
    for i in range(1, 100000001):
        result += 1 / i
    return result


# numpy
def one_line_evaluation():
    return sum([1 / i for i in range(1, 100000001)])


def print_stats(function, function_name):
    start = time.time()
    k = function()
    end = time.time()
    print(f"Result using {function_name} evaluation:", round(k, 4))
    print(f"Time using {function_name} evaluation: {round(end - start, 4)}s")


if __name__ == "__main__":
    multiprocessing_start = time.time()
    total_result = multiprocessing.Value('d', 0.0)
    processes = []
    lock = multiprocessing.Lock()

    ranges = [(1, 12500000), (12500001, 25000000), (25000001, 37500000), (37500001, 50000000),
              (50000001, 62500000), (62500001, 75000000), (75000001, 87500000), (87500001, 100000000)]

    for start, end in ranges:
        p = multiprocessing.Process(target=multiprocessing_evaluation,
                                    args=(total_result, lock, start, end))
        p.start()
        processes.append(p)

    for p in processes: p.join()

    multiprocessing_end = time.time()

    # Sum from 1 to 100 million should take up to 2s
    print("Result using multiprocessing:", round(total_result.value, 4))
    print(f"Time using multiprocessing: {round(multiprocessing_end - multiprocessing_start, 4)}s")

    #sum from 1 to 100 million should take up to 5s
    print_stats(simple_evaluation, "simple")

    #sum from 1 to 100 million should take up to 7-8s
    print_stats(one_line_evaluation, "one liner")
