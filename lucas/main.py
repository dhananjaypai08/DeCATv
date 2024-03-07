# Web3 imports
from web3 import Web3, AsyncWeb3
import json
# Fastapi imports
from fastapi import FastAPI, Request, Response, Query, Body
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
from dataclasses import dataclass
import cloudinary 
import cloudinary.uploader

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
    Lighthouse_GATEWAY_URL,
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
model = genai.GenerativeModel('gemini-pro')

cloudinary.config( 
  cloud_name = "dzvstpvlt", 
  api_key = "188374828552585", 
  api_secret = "vMCoE46Phj4zK5k7Bd13NOHuW78" 
)

skills = {
    "python": 1,
    "java": 1,
    "c++": 1,
    "git": 1,
    "javascript": 1,
}

@dataclass
class MetaData:
    name: str
    description: str
    imageuri: str
    tokenId: int

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
        tokenURI = await contractwithsigner.functions.tokenURI(tokenId[3]).call()
        ans.append({"tokenId": tokenId[3], "tokenURI": Lighthouse_GATEWAY_URL+tokenURI})
    logger.success(f"Fetched SBT data for wallet address: {id}")
    return ans

@app.get("/endorsements_received")
async def home(id: str):
    ids = await contractwithsigner.functions.getTokenIdAccountEndorsing(id).call()
    logger.info("Data Retrieved")
    ans = []
    for tokenId in ids:
        tokenURI = await contractwithsigner.functions.tokenURI(tokenId[3]).call()
        ans.append({"tokenId": tokenId[3], "tokenURI": Lighthouse_GATEWAY_URL+tokenURI})
    logger.success(f"Fetched endorsing data for wallet address: {tokenId[3]}")
    return ans

@app.post("/generate_qrcode")
async def generate(request: Request):
    data = await request.json()
    str_data = json.dumps(data)
    print(str_data, type(str_data))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    image_stream = BytesIO()
    img.save(image_stream, format="PNG")
    image_stream.seek(0)
    result = cloudinary.uploader.upload(image_stream,public_id='qrcode')
    return result["secure_url"]
    # return FileResponse("qrcode.png", media_type="application/octet-stream", filename="qrcode.png")

@app.post("/scanQR")
async def scanQR():
    cap = cv2.VideoCapture(0)
    found_qr_data = False
    verified_data = False
    res = {}
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
            tokenId = dict_data["tokenId"]
            logger.info(f"Fetched type: {typeofSBT}, address: {address}, TokenId: {str(tokenId)}")
            flg = 0
            if flg == 0:
                tokenIds = await contractwithsigner.functions.getTokenIdAccount(address).call()
                print(tokenIds)
                for id in tokenIds:
                    # uri = await contractwithsigner.functions.tokenURI(id).call()
                    # if uri == URI: 
                    #     verified_data = True
                    if id[3] == tokenId:
                        verified_data = True
                        flg = 1
            elif flg == 0:
                tokenIds = await contractwithsigner.functions.getTokenIdAccountEndorsing(address).call()
                print(tokenIds)
                for id in tokenIds:
                    # uri = await contractwithsigner.functions.tokenURI(id).call()
                    # if uri == URI:
                    #     verified_data = True
                    if id[3] == tokenId: verified_data = True

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
                res_string = f"The NFT with tokenId: {str(tokenId)} of wallet Address: {address} is Verified"
                res["msg"] = res_string
                res["tokenId"] = tokenId
                res["verified"] = True
                res["name"] = dict_data["name"]
                res["description"] = dict_data["description"]
                res["image"] = dict_data["image"]
            else:
                res_string = f"Unfortunately, The NFT with tokenId: {str(tokenId)} of wallet Address: {address} is NOT Verified"
                res["msg"] = res_string
                res["verified"] = False
            data = json.dumps(res)
            print(data)
            return Response(data)

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    return Response("QRCode not detected")

@app.post("/getCasualInsights")
async def getInsights(data: list = Body(...)):
    if not data: return "Add something to your certificates List"
    response = model.generate_content("Generate text which should be strictly less 100 words limit and Make sure the generated text is in plain string text and should be without any '*' or neither any other such characters for designing. Generate text about casual Granular statistical overview Insights on this data which signifies all the certificates earned in a particular field : "+str(data)+". The text should contain this data for eg: x percent proficient in y field(example: 50% proficient in python with 2 certificates in python) and the total words of generated words is less than or equal to 100 words.")
    return response.text

@app.get("/getJobs")
async def getJobs():
    accounts = await contractwithsigner.functions.getAccounts().call()
    print(accounts)
    data = {}
    for account in accounts:
        metadata = await contractwithsigner.functions.getTokenIdAccount(account).call()
        data[account] = metadata
        dataset = []
        for i in metadata:
            dataset.append(i[0]+" "+i[1])
        prompt = "How many skills jobs are available in India today for all the skills mentioned in the given datatset . Just provide the skill name mapped with an integer value(the number of jobs for that skills) that I can convert to dictionary directly in python. The dataset is : "+str(dataset)
        print(prompt)
        response = model.generate_content(prompt)
        break
    return response.text

if __name__ == "__main__":
    uvicorn.run("main:app", port=8082, log_level="info", reload=True)
