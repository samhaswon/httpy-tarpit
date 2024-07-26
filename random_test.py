from random_junk import random_junk
import time


if __name__ == '__main__':
    test_junk = random_junk.random_junk(2)
    print(type(test_junk))
    test_junk = test_junk.decode("ascii")
    print(len(test_junk))
    # print(test_junk)

    time_accumulator = 0.0
    repetitions = 1_000
    for i in range(repetitions):
        start = time.perf_counter()
        random_junk.random_junk(128)
        end = time.perf_counter()
        time_accumulator += end - start

    print(f"Time to generate data: {time_accumulator:.6f}\n"
          f"{time_accumulator / repetitions * 1_000_000:.6f}µs per chunk")
