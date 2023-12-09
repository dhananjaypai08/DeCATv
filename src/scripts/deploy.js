const hre = require("hardhat");

async function main() {
  const dcat = await hre.ethers.getContractFactory("DeCAT");
  const contract = await dcat.deploy(); //instance of contract

  await contract.deployed();
  console.log("Address of contract:", contract.address);
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
