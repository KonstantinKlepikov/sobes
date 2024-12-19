import multiprocessing
import time


def long(v) -> None:
    for _ in range(1000000):
        v.value += 1


def start_parallel(num_of_proc: int) -> int:
    print('=' * 10, 'Proc')
    start_time = time.time()
    counter = multiprocessing.Value('i', 0, lock=False)
    for _ in range(num_of_proc):
        proc = multiprocessing.Process(target=long, args=(counter,))
        proc.start()
        proc.join()

    print(f'--- {time.time() - start_time} seconds ---')
    return counter.value


def start_sync(num_of_proc: int) -> int:
    print('=' * 10, 'sync')
    start_time = time.time()
    counter = multiprocessing.Value('i', 0)
    for _ in range(num_of_proc):
        long(counter)
    print(f'--- {time.time() - start_time} seconds ---')
    return counter.value


if __name__ == '__main__':
    cpu = multiprocessing.cpu_count()
    print(cpu)
    results1 = start_parallel(cpu)
    print(results1)
    results2 = start_sync(cpu)
    print(results2)

    print(f'Proc: {results1}')
    print(f'Sync: {results2}')
