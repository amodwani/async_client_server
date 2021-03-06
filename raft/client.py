import asyncio
import sys,platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
event_loop = asyncio.get_event_loop()

async def echo_client(address):
    reader, writer = await asyncio.open_connection(*address)
    while True:
        command = input('command=')
        # command = 'aa'
        if command:
            # writer.write(str.encode('{"source":"client-'+ address[0] + '-' + address[1] + '","command":"'+ command +'"}'))
            writer.write(str.encode('client=>'+command))
            await writer.drain()

            print('waiting for response')

            data = await reader.read(255)
            if data:
                print('received {!r}'.format(data))
            else:
                print('closing')
                writer.close()
                return

try:
    event_loop.run_until_complete(
        echo_client(['localhost',sys.argv[1]])
    )
finally:
    print('closing event loop')
    event_loop.close()