# Web3 imports
from web3 import Web3, AsyncWeb3
import json
# Fastapi imports
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from config import Node, Contract, Google
import uvicorn
from middleware.TimeMiddleware import TimeMiddleware
from fastapi.middleware.cors import CORSMiddleware
# other imports
from loguru import logger
from io import BytesIO
import qrcode
import cv2
from pyzbar.pyzbar import decode
import google.generativeai as genai

w3 = None
contractwithsigner = None
app = FastAPI()
contract = Contract()
node = Node()
app.add_middleware(TimeMiddleware)
Lighthouse_GATEWAY_URL = "https://gateway.lighthouse.storage/ipfs/"

origins = [
    "http://localhost",
    "http://localhost:8082",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = Google().api_key
genai.configure(api_key=api_key)

async def read_json():
    file = open(contract.abi_path)
    data = json.load(file)
    file.close()
    return data["abi"]

@app.on_event("startup")
async def startup_event():
    global w3
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(node.url))
    contract_abi = await read_json()
    global contractwithsigner
    contractwithsigner = w3.eth.contract(address=contract.address, abi=contract_abi)
    logger.info(f"Connected with smart contract with address {contract.address}")
    
@app.get("/")
async def home(id: str):
    val = await contractwithsigner.functions.getTotalMints().call()
    logger.info(f"Total DeCAT Volume: {val}")
    tokenIds = await contractwithsigner.functions.getTokenIdAccount(id).call()
    ans = []
    for tokenId in tokenIds:
        tokenURI = await contractwithsigner.functions.tokenURI(tokenId).call()
        ans.append({"tokenId": tokenId, "tokenURI": Lighthouse_GATEWAY_URL+tokenURI})
    logger.success(f"Fetched SBT data for wallet address: {id}")
    return ans

@app.get("/endorsements_received")
async def home(id: str):
    ids = await contractwithsigner.functions.getTokenIdAccountEndorsing(id).call()
    logger.info("Data Retrieved")
    ans = []
    for tokenId in ids:
        tokenURI = await contractwithsigner.functions.tokenURI(tokenId).call()
        ans.append({"tokenId": tokenId, "tokenURI": Lighthouse_GATEWAY_URL+tokenURI})
    logger.success(f"Fetched endorsing data for wallet address: {id}")
    return ans

@app.post("/generate_qrcode")
async def generate(request: Request):
    data = await request.json()
    str_data = json.dumps(data)
    print(type(str_data))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    return FileResponse("qrcode.png", media_type="application/octet-stream", filename="qrcode.png")

@app.post("/scanQR")
async def scanQR():
    cap = cv2.VideoCapture(0)
    found_qr_data = False
    verified_data = False
    while True:
        ret, frame = cap.read()

        # Find and decode QR codes
        decoded_objects = decode(frame)
        
        # Display the image
        cv2.imshow("QR Code Scanner", frame)

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            dict_data = json.loads(data)
            print(dict_data, type(dict_data))
            found_qr_data = True
            typeofSBT = dict_data["name"]
            address = dict_data["walletAddress"]
            URI = dict_data["tokenURI"]
            logger.info(f"Fetched type: {typeofSBT}, address: {address}, URI: {URI}")
            if typeofSBT == "DeCAT":
                tokenIds = await contractwithsigner.functions.getTokenIdAccount(address).call()
                for id in tokenIds:
                    uri = await contractwithsigner.functions.tokenURI(id).call()
                    if uri == URI: 
                        verified_data = True
            elif typeofSBT == "E-DeCAT":
                tokenIds = await contractwithsigner.functions.getTokenIdAccountEndorsing(address).call()
                for id in tokenIds:
                    uri = await contractwithsigner.functions.tokenURI(id).call()
                    if uri == URI:
                        verified_data = True

        # Break the loop if 'q' key is pressed
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            # Release the camera and close the window
            cap.release()
            cv2.destroyAllWindows()
            return Response("Exited with no response")
        if cv2.waitKey(1) & found_qr_data:
            # Release the camera and close the window
            cap.release()
            cv2.destroyAllWindows()
            if verified_data:
                res_string = f"The NFT with tokenURI: {URI} of wallet Address: {address} is Verified"
            else:
                res_string = f"Unfortunately, The NFT with tokenURI: {URI} of wallet Address: {address} is NOT Verified"
            return Response(res_string)

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    return Response("QRCode not detected")

@app.route("/getCasualInsights")
async def getInsights(address: str):
    return address

if __name__ == "__main__":
    uvicorn.run("main:app", port=8082, log_level="info", reload=True)
