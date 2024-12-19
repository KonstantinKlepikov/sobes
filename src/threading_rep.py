import threading
import time

import requests  # type: ignore

CAT_FACTS = 'https://meowfacts.herokuapp.com/'
# {"data":
# ["Many times this disease can be treated successfully."]}


def get_cat_fact(results: list[str]) -> None:
    """Get cat fact"""
    response = requests.get(CAT_FACTS)
    results.append(response.json()['data'][0])


def start_async(r: int) -> list[str]:
    print('=' * 10, 'threads')
    start_time = time.time()
    threads: list[threading.Thread] = []
    results: list[str] = []
    for _ in range(r):
        t = threading.Thread(target=get_cat_fact, args=(results,))
        threads.append(t)
        t.start()
    for i in threads:
        i.join()
    print(f'--- {time.time() - start_time} seconds ---')
    return results


def start_sync(r: int) -> list[str]:
    print('=' * 10, 'sync')
    start_time = time.time()
    results: list[str] = []
    for _ in range(r):
        get_cat_fact(results)
    print(f'--- {time.time() - start_time} seconds ---')
    return results


if __name__ == '__main__':
    results1 = start_async(20)
    print(len(results1))
    results2 = start_sync(20)
    print(len(results2))

    print(f'Async: {results1}')
    print(f'Sync: {results2}')
