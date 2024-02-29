class Node:
    def __init__(self):
        self.url = 'https://eth-sepolia.g.alchemy.com/v2/YrcRBtPyzQZxWtNt-Cd8sYXh46GSSczW'
        self.name = 'Eth-Sepolia Alchemy'
        self.api_key = 'YrcRBtPyzQZxWtNt-Cd8sYXh46GSSczW'
        
class Contract:
    def __init__(self):
        self.name = "DeCAT"
        self.inherits = "ERC721"
        self.address = "0x61eFE56495356973B350508f793A50B7529FF978"
        self.abi_path = "../src/contracts/decat.json"
    
class Google:
    def __init__(self):
        self.api_key = "AIzaSyA652ybiYvXVkSYieJgT8VynRauQlxuEbA"