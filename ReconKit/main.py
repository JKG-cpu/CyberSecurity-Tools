from src import *

asyncio.run(Scanner("localhost", 9990, 10000).start_scan())