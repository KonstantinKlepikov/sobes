import asyncio


async def task_run():
    await asyncio.sleep(1)


async def tasc_cancel(task):
    task.cancel()


async def main():
    print('creating task')
    task1 = asyncio.create_task(task_run(), name='task_run')
    task2 = asyncio.create_task(tasc_cancel(task1), name='task_cancel')
    try:
        await task1
        print(f'task completed: {task1.get_name()}')
    except asyncio.CancelledError:
        print('task canceled')

    await task2
    print(f'task completed: {task2.get_name()}')


asyncio.run(main())
