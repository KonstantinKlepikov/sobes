import asyncio


async def phase(i):
    print(f'in phase {i}')
    await asyncio.sleep(0.5 - (0.1 * i))
    print(f'done with phase {i}')
    return f'phase {i} result'


async def main(num_phases):
    phases = [phase(i) for i in range(num_phases)]
    results = []
    for next_to_complete in asyncio.as_completed(phases):
        answer = await next_to_complete
        results.append(answer)
    print(results)


asyncio.run(main(3))
