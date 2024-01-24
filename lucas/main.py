# Web3 imports
from web3 import Web3, AsyncHTTPProvider
import json
# Fastapi imports
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from config import Node, Contract
import uvicorn
from middleware.TimeMiddleware import TimeMiddleware
# other imports
from loguru import logger
from io import BytesIO
import qrcode
import cv2
from pyzbar.pyzbar import decode

w3 = None
contractwithsigner = None
app = FastAPI()
contract = Contract()
node = Node()
app.add_middleware(TimeMiddleware)

async def read_json():
    file = open(contract.abi_path)
    data = json.load(file)
    file.close()
    return data["abi"]

@app.on_event("startup")
async def startup_event():
    global w3
    w3 = Web3(Web3.HTTPProvider(node.url))
    contract_abi = await read_json()
    global contractwithsigner
    contractwithsigner = w3.eth.contract(address=contract.address, abi=contract_abi)
    logger.info(f"Connected with smart contract with address {contract.address}")
    
@app.get("/{id}")
async def home(id: str):
    val = contractwithsigner.functions.getTotalMints().call()
    logger.info(f"Total DeCAT Volume: {val}")
    tokenIds = contractwithsigner.functions.getTokenIdAccount(id).call()
    ans = []
    for tokenId in tokenIds:
        tokenURI = contractwithsigner.functions.tokenURI(tokenId).call()
        ans.append({tokenId: tokenURI})
    logger.success(f"Fetched data for wallet address: {id}")
    return ans

@app.post("/generate_qrcode")
async def generate(request: Request):
    print(request)
    data = request.body
    print(data, type(data))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    return Response("Image saved locally")

@app.post("/scanQR")
async def scanQR():
    cap = cv2.VideoCapture(0)
    found_qr_data = False
    res_data = None
    while True:
        ret, frame = cap.read()

        # Find and decode QR codes
        decoded_objects = decode(frame)
        
        # Display the image
        cv2.imshow("QR Code Scanner", frame)

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            print(type(data))
            print(f"QR Code Data: {data}")
            res_data = data
            found_qr_data = True

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & found_qr_data:
            # Release the camera and close the window
            cap.release()
            cv2.destroyAllWindows()
            return Response(res_data)

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    return Response("QRCode not detected")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8082, log_level="info", reload=True)
