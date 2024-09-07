# fastapi bigdata server example
This code is bigdata server program written in Python using the FastAPI framework. It is designed to handle file exchanges between a client and a server via HTTP POST requests and WebSocket connections. Here's an overview of the key features:

# Features:
1. **Logging and Debugging**:
   - The script uses Python's `logging` module for debugging purposes.
   - Logging is set to the `DEBUG` level to capture detailed information about the application's execution.

2. **CORS Middleware**:
   - The server includes CORS (Cross-Origin Resource Sharing) middleware to allow requests from any origin, with any method and headers.
   
3. **Calculation Endpoint**:
   - **POST `/v1/calc`**: 
     - This endpoint accepts a `length` parameter.
     - A background task is initiated that simulates a calculation (with a 15-second delay).
     - The result of the calculation is hardcoded to `3.14` and returned as a JSON response.

4. **WebSocket Endpoints**:
   - **WebSocket `/v1/get_dataset`**:
     - This endpoint sends the content of a JSON file to the client in chunks of 64KB.
     - It reads a file (`server_ifc_file.json`) and streams it to the client.
   - **WebSocket `/v1/put_dataset`**:
     - This endpoint receives a zipped file from the client.
     - The file is written to a temporary location (`temp/temp_dataset.zip`), extracted, and stored in a specified directory (`./server_data`).

# Key Considerations:
- **Timeout Handling**: The script handles potential timeouts during data reception, retrying the connection up to 5 times.
- **Error Handling**: The script includes basic error handling for WebSocket disconnections and file processing issues.

# Usage:
- To run the server, use the following command:
  ```
  uvicorn server:app --reload --port 8001 --ws-max-size 16777216
  ```
  - This starts the FastAPI server on port 8001, with a maximum WebSocket size of 16 MB.

# Author
Taewook Kang (laputa99999@gmail.com)

# License
MIT License
