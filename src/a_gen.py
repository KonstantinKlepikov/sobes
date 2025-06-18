import asyncio
import random
from typing import AsyncGenerator


async def agen() -> AsyncGenerator[str, None]:
    while True:
        rndi = random.randint(0, 10)
        if rndi == 10:
            print('is 10')
            break
        yield f'something: {random.randint(0, 100)}'


async def main():
    async for i in agen():
        print(i)


if __name__ == '__main__':
    asyncio.run(main())
