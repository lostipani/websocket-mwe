import json
import asyncio
import numpy as np
from typing import List, Any
from websockets.asyncio.client import connect


async def main(data: List[Any], uri: str = "ws://localhost:12345"):
    async with connect(uri) as websocket:
        async for message in websocket:
            data.append(json.loads(message)["value"])
            arr = np.array(data)
            print(f"mean: {np.mean(arr)} and std: {np.std(arr)}")


if __name__ == "__main__":
    data = list()
    asyncio.run(main(data))
