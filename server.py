# author: Taewook Kang (laputa99999@gmail.com)
# purpose: This is a server script that receives a file from the client, processes the file, and sends the processed data back to the client.
# license: MIT license
# usage: uvicorn server:app --reload --port 8001 --ws-max-size 16777216
# date: 2024-09-05
#
import json, time, logging, asyncio, zipfile, os, websockets
from fastapi import FastAPI, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect

# Set up logging to debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# uvicorn open_api_server:app --reload --port 8001 --ws-max-size 16777216   # https://www.uvicorn.org
app = FastAPI()

# CORS middleware. considering security
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # Allows all origins
	allow_credentials=True,
	allow_methods=["*"],  # Allows all methods
	allow_headers=["*"],  # Allows all headers
)
	
def calc_function(length: str):
	logger.debug('calculation started...')

	time.sleep(15)  # 15 seconds
	# TODO call your calculation functions
	data = 3.14

	logger.debug(f'End')
	return data

@app.post("/v1/calc")
async def calculate(background_tasks: BackgroundTasks, length: str):
	logger.debug('calculation started...')
	results = calc_function(length)
	return {"results": results}

@app.websocket("/v1/get_dataset") # don't remove /ws prefix to use websocket
async def get_dataset(websocket: WebSocket):
	logger.debug('Trying to connect...')
	await websocket.accept()
	logger.debug('Connection accepted.')

	try:
		# with open('./example_fastapi/server_ifc_file.json') as json_file:
		with open('./server_ifc_file.json') as json_file:
			data = json.load(json_file)
			data = json.dumps(data)

			logger.debug('Message length: ' + str(len(data)))
			CHUNK_SIZE = 64 * 1024  # 64KB
			for i in range(0, len(data), CHUNK_SIZE):
				chunk = data[i:i+CHUNK_SIZE]
				print(f'chunk: {i}')
				await websocket.send_text(chunk)
			logger.debug('JSON data sent.')
	except Exception as e:
		logger.error(f"Error sending data: {e}")

@app.websocket("/v1/put_dataset")
async def put_dataset(websocket: WebSocket):
	logger.debug('trying to connect...')
	await websocket.accept()
	logger.debug('connection accepted.')

	# temp_zip_path = './example_fastapi/temp/temp_dataset.zip'
	temp_zip_path = './temp/temp_dataset.zip'
	try:
		with open(temp_zip_path, 'wb') as temp_zip_file:
			try_index = 0
			while True:	
				try:
					data = await websocket.receive_bytes()
					if not data:
						break
					temp_zip_file.write(data)
				except asyncio.TimeoutError:
					logger.debug("Timeout: The client didn't respond within 5 seconds")
					try_index += 1
					if try_index > 5:
						logger.error("Timeout: The client didn't respond within 5 seconds for 5 times")
						return
					pass
	except WebSocketDisconnect as e:
		logger.debug(f"Connection closed: {e}")
		pass
	except Exception as e:
		logger.error(f"Error receiving data: {e}")
		return

	logger.debug('Zip file received.')

	# Extract the zip file
	# extract_path = './example_fastapi/server_data'
	extract_path = './server_data'
	os.makedirs(extract_path, exist_ok=True)
	with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
		zip_ref.extractall(extract_path)

	logger.debug('Zip file extracted.')
	await websocket.close()
