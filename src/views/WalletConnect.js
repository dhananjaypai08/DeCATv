import React, { useState } from 'react';
import { useWeb3Connect } from 'web3connect';
import { Button } from 'react-bootstrap'; // You can use your preferred button component

const WalletConnect = () => {
  const [connector, setConnector] = useState(null);
  const { connect, accounts, error } = useWeb3Connect();

  const handleConnect = async (selectedConnector) => {
    try {
      const newConnector = await connect(selectedConnector);
      setConnector(newConnector);
    } catch (error) {
      console.error('Connection error:', error);
    }
  };

  const renderButton = (connectorName) => (
    <Button
      variant="primary"
      onClick={() => handleConnect(connectorName)}
      disabled={connector} // Disable button if already connected
    >
      Connect with {connectorName}
    </Button>
  );

  return (
    <div>
      {error && <p style={{ color: 'red' }}>{error.message}</p>}
      {!connector && (
        <>
          {renderButton('MetaMask')}
          {renderButton('WalletConnect')}
          {renderButton('Coinbase Wallet')}
          {/* Add buttons for other supported connectors */}
        </>
      )}
      {connector && (
        <p>Connected with: {accounts[0]}</p>
      )}
    </div>
  );
};

export default WalletConnect;
