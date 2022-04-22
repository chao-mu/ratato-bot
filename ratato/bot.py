# Core
import asyncio

class Bot:
    async def start(self):
        task = asyncio.create_task(self._run())

        while True:
            await asyncio.sleep(1)
            if self.is_connected:
                break

        while True:
            msg = await self.inbox.get()
            await self.write_message(msg)
