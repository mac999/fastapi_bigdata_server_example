# author: Taewook Kang (laputa99999@gmail.com)
# purpose: This is a client script that sends a file to the server, requests the server to process the file, and receives the processed data from the server.
# license: MIT license
# usage: python client.py
# date: 2024-09-05
#
import json, traceback, asyncio, websockets, aiohttp # import httpx
from aiohttp import ClientSession, ClientTimeout

async def put_dataset(file_path):
    async with websockets.connect('ws://localhost:8001/v1/put_dataset') as websocket:
        CHUNK_SIZE = 64 * 1024  # 64KB
        try:
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    await websocket.send(chunk)
                    print(f'Sent chunk of size: {len(chunk)}')
            print("File sent successfully.")
        except Exception as e:
            print(f"Error sending file: {e}")

async def calc_dataset():
    params = {"length": "10"}
    t = ClientTimeout(total=60*2)  # 2 minutes
    async with aiohttp.ClientSession(timeout=t) as session:
        async with session.post('http://localhost:8001/v1/calc', params=params) as resp:
            results = await resp.text()
            print(results)

async def get_dataset():
    async with websockets.connect('ws://localhost:8001/v1/get_dataset') as websocket:
        CHUNK_SIZE = 64 * 1024  # 64KB
        full_data = None
        received_count = 0
        try:
            while True:
                chunk = await asyncio.wait_for(websocket.recv(), timeout=5) # adjust timeout value considering internet speed
                if full_data is None:
                    full_data = chunk
                else:
                    full_data += chunk
                received_count += len(chunk) 
                print('Received data: ', received_count)
        except asyncio.TimeoutError:
            print("Timeout: The server didn't respond within 5 seconds")
        except Exception as e:
            print(e)
            pass
        
        print('Received data: ', received_count)
        data = json.loads(full_data)
        try:
            os.remove('big_xml.json')
        except:
            pass
        with open('big_xml.json', 'w') as json_file:
            json.dump(data, json_file)
            print('JSON data saved to file.')

def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(put_dataset('./client_data/input_data.zip'))
        loop.run_until_complete(calc_dataset())
        loop.run_until_complete(get_dataset())
    except Exception as e:
        print(traceback.format_exc())

if __name__ == '__main__':
    main()