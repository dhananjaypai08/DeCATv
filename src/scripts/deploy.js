const hre = require("hardhat");

async function main() {
  const sbt = await hre.ethers.getContractFactory("SBT");
  const contract = await sbt.deploy(); //instance of contract

  await contract.deployed();
  console.log("Address of contract:", contract.address);
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});