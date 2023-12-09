// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

// import "@openzeppelin/contracts@4.7.0/token/ERC721/ERC721.sol";
// import "@openzeppelin/contracts@4.7.0/token/ERC721/extensions/ERC721URIStorage.sol";

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
// import "@openzeppelin/contracts@4.7.0/access/Ownable.sol";
import "./Set.sol";

contract SBT is ERC721, ERC721URIStorage {
    mapping(address => string) public creds; // whitelisting 
    uint256 public total_mints;
    mapping(address => uint256) public total_sbt_received_in_account; // total SBT's recieved in the user account
    mapping(address => uint256) private endorsements_allowed;
    mapping(address => uint256) private endoresement_received; // endorsements recieved
    mapping(address => uint256[]) private tokenIds_in_account; 
    uint256 private tokenId;
    address public owner;
    address private burning_address = 0x000000000000000000000000000000000000dEaD;
    Set private accounts = new Set();

    event Minted(address _to, uint256 _tokenId, string _uri);
    event MultipleMinted(address[] _to, string[] _uri);
    event EndorsedMint(address _from, address _to, string _uri);

    constructor() ERC721("SoulBoundToken", "SBT") {
        creds[0xdC737Bc0B2174a5d4A8CA7b588905c7770C671ee] = "123";
        creds[0x5B38Da6a701c568545dCfcB03FcB875f56beddC4] = "456";
        owner = msg.sender;
    }

    // modifier to check 
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function safeMint(address to, string memory uri) public onlyOwner {
        tokenId += 1;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        accounts.add(to);
        total_mints += 1;
        total_sbt_received_in_account[to] += 1;
        endorsements_allowed[to] += 1;
        tokenIds_in_account[to].push(tokenId);
        emit Minted(to, tokenId, uri);
    }

    modifier checkEndorsement() {
        require((endorsements_allowed[msg.sender] > 0 && total_sbt_received_in_account[msg.sender]>0) || msg.sender == owner, "Endorsement not allowed");
        _;
    }

    function endorseMint(address to, string memory uri) public checkEndorsement() {
        tokenId += 1;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        accounts.add(to);
        total_mints += 1;
        total_sbt_received_in_account[to] += 1;
        endoresement_received[to] += 1;
        endorsements_allowed[msg.sender] -= 1;
        tokenIds_in_account[to].push(tokenId);
        emit EndorsedMint(msg.sender, to, uri);
    }

    function mintBatch(address[] memory _to, string[] memory _uri) external onlyOwner {
        for (uint256 i = 0; i < _to.length; i++) {
            tokenId += 1;
            _safeMint(_to[i], tokenId);
            _setTokenURI(tokenId, _uri[i]);
            total_mints += 1;
            total_sbt_received_in_account[_to[i]] += 1;
            endorsements_allowed[_to[i]] += 1;
            tokenIds_in_account[_to[i]].push(tokenId);
        }
        emit MultipleMinted(_to, _uri);
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 _tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(_tokenId);
    }

    function tokenURI(uint256 _tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(_tokenId);
    }

    function getVal(address _new) public view returns(string memory) {
        return creds[_new];
    }

    // Sould Bound property 
    function _beforeTokenTransfer(address from, address to, uint256 _tokenId) internal override virtual { 
        require(from == address(0) || to == burning_address, "Err: token transfer is BLOCKED"); 
        super._beforeTokenTransfer(from, to, _tokenId);
        if(to == burning_address){
            total_sbt_received_in_account[from] -= 1;
            uint256 j;
            for(uint256 i = 0; i<tokenIds_in_account[from].length; i++){
                if(tokenIds_in_account[from][i] == _tokenId){
                    j = i;
                    break;
                }
            }
            tokenIds_in_account[from][j] = tokenIds_in_account[from][tokenIds_in_account[from].length-1];
            tokenIds_in_account[from].pop();
        }
    }

    // Function to get the total mint count
    function getTotalMints() public view returns (uint256) {
        return total_mints;
    }

    function getTokenId() public view returns(uint256) {
        return tokenId;
    }

    function getEndorsements(address _address) public view returns(uint256){
        return endoresement_received[_address];
    }

    function getEndorsementCheck(address _address) public view returns(uint256) {
        return endorsements_allowed[_address];
    }

    function getTokenIdAccount(address _address) public view returns(uint256[] memory) {
        return tokenIds_in_account[_address];
    }

    function getAccounts() public view returns(address[] memory) {
        return accounts.getItems();
    }
}