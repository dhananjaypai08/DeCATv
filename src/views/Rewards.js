import React from "react";

import Script from "dangerous-html/react";
import { Helmet } from "react-helmet";
import { useState, useEffect } from "react";
import { Redirect } from 'react-router-dom'
import abi from "../contracts/Autocrate.json";
//import './App.css';
import { ethers } from "ethers";
import axios from "axios";

import "./home.css";
import { useAppContext } from "../AppContext";
const fetch = require('node-fetch');

const Rewards = () => {
  

  const getBalance = async(event) => {
    event.preventDefault();
    const walletid = document.querySelector('#walletid').value;
    const url = `https://api.circle.com/v1/w3s/wallets/${walletid}/balances`;
    const options = {
    method: 'GET',
    headers: {'Content-Type': 'application/json', Authorization: 'Bearer TEST_API_KEY:ee43073e8f53859f8c670da3fefd69c4:e12f1fb80da373c31d4db2f5af67052f'}
    };

    fetch(url, options)
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(err => console.error('error:' + err));
        event.target.reset();
    }

    const sendMATIC = async(event) => {
        event.preventDefault();
        const walletaddress = document.querySelector('#walletid').value;
        const amount = document.querySelector('#amount').value;
        const url = 'https://api.circle.com/v1/w3s/developer/transactions/transfer';
        const options = {
        method: 'POST',
        headers: {'Content-Type': 'application/json', Authorization: 'Bearer TEST_API_KEY:ee43073e8f53859f8c670da3fefd69c4:e12f1fb80da373c31d4db2f5af67052f'},
        body: JSON.stringify({
            idempotencyKey: 'b242be54-f057-4ed1-a638-d20605ec6180',
            entitySecretCipherText: 'hyBXEY+GUF3Jt9u6fE8qFxo9cGy5eXZxH84c8ReU+3mArXZsfKf4MW34eQaBctulsYCeevpprQSdrfBh4WVrdLgCDthwYfC5Z9deJ3jFUdczwTS+H5O6T2BeAyCecbTN0/Sc8vtRsmw+WT6B8tnP1NH++MwFA7KafHSMcjhwYZVDnl+VokA55lcng/iCanY3l3PSylJMp2APVh3fI6QBd1JRyJLOc7xWaY1Daij9Azlug449dTLpTj8/UF82Ao0KoL5Kx6/1qX+creaS/BrC2obfqumJjL/9vgBXR2Fpha9WzcNcFZJIGJF6l6l+vjfuiSnSnKIMaAA79QIYUbFlmZ/lQDffzcEqZYgt/aA65gtdgI0x9rKR91UlxUs2lB+K75/JfmtLyfcCyddIvJQXR11j5ghT4gZW/sNMq6v6B0Iu4YSX6nV34Fzv64N9tFCQ6UdO2hslmdhmdA8ZxXstgkHHEWUexTK6gD92CB+owOwzXKD8uKZGfSrg3PKSJtQH20M0FomnzmFsaEb8/CwBWeAH8SB14ixUVclMEa/UK9zTqyS8MqUKp3leeXVS+63FlXZRwz5aRg5qIh93dWM9faGC5JuebX9f7xrhhBDnnUEGZFAyXEXZ7q30QPZaW4f2mskRAm8BRmivRiz51owyz+k/ShH7sKptkEEA0yhJHcM=',
            amounts: [amount],
            destinationAddress: walletaddress,
            feeLevel: 'HIGH',
            tokenId: 'e4f549f9-a910-59b1-b5cd-8f972871f5db',
            walletId: 'a62612d7-91b6-5180-85e0-75501a90b039'
        })
        };
        fetch(url, options)
        .then(res => res.json())
        .then(json => console.log(json))
        .catch(err => console.error('error:' + err));
        event.target.reset();
    }
  return (
    <div className="home-container">
      <Helmet>
        <title>Home</title>
        <meta property="og:title" content="Dashboard" />
        <link href="https://db.onlinewebfonts.com/c/974bd878107a4b17fbb34db4029679e9?family=Clepto+Regular" rel="stylesheet"></link>
      </Helmet>
      <header data-thq="thq-navbar" className="home-navbar">
        <span className="home-logo"><a  href="/">
              Autocrate
            </a></span>
        <div
          data-thq="thq-navbar-nav"
          data-role="Nav"
          className="home-desktop-menu"
        >
          <nav
            data-thq="thq-navbar-nav-links"
            data-role="Nav"
            className="home-nav"
          >
            <a href="/rewards" className="home-button2 button-clean button">
              Rewards
              </a>
            
            
          </nav>
        </div>
        <div data-thq="thq-navbar-btn-group" className="home-btn-group">
          
          {/* <button onClick={checkConnectionBeforeConnecting} className="button wallet-btn">
            {connectmsg}
          </button> */}
        </div>
        <div data-thq="thq-burger-menu" className="home-burger-menu">
          <button className="button home-button5">
            <svg viewBox="0 0 1024 1024" className="home-icon">
              <path d="M128 554.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 298.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 810.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667z"></path>
            </svg>
          </button>
        </div>
        <div data-thq="thq-mobile-menu" className="home-mobile-menu">
          <div
            data-thq="thq-mobile-menu-nav"
            data-role="Nav"
            className="home-nav1"
          >
            <div className="home-container1">
              <span className="home-logo1">Autocrate</span>
              <div data-thq="thq-close-menu" className="home-menu-close">
                <svg viewBox="0 0 1024 1024" className="home-icon02">
                  <path d="M810 274l-238 238 238 238-60 60-238-238-238 238-60-60 238-238-238-238 60-60 238 238 238-238z"></path>
                </svg>
              </div>
            </div>
            <nav
              data-thq="thq-mobile-menu-nav-links"
              data-role="Nav"
              className="home-nav2"
            >
            <a href="/multiple" className="home-button2 button-clean button">
              Multiple Transaction
            </a>

            </nav>
            <div className="home-container2">
              <button className="home-login button">Login</button>
              <button className="button">Register</button>
            </div>
          </div>
          <div className="home-icon-group">
            <svg viewBox="0 0 950.8571428571428 1024" className="home-icon04">
              <path d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z"></path>
            </svg>
            <svg viewBox="0 0 877.7142857142857 1024" className="home-icon06">
              <path d="M585.143 512c0-80.571-65.714-146.286-146.286-146.286s-146.286 65.714-146.286 146.286 65.714 146.286 146.286 146.286 146.286-65.714 146.286-146.286zM664 512c0 124.571-100.571 225.143-225.143 225.143s-225.143-100.571-225.143-225.143 100.571-225.143 225.143-225.143 225.143 100.571 225.143 225.143zM725.714 277.714c0 29.143-23.429 52.571-52.571 52.571s-52.571-23.429-52.571-52.571 23.429-52.571 52.571-52.571 52.571 23.429 52.571 52.571zM438.857 152c-64 0-201.143-5.143-258.857 17.714-20 8-34.857 17.714-50.286 33.143s-25.143 30.286-33.143 50.286c-22.857 57.714-17.714 194.857-17.714 258.857s-5.143 201.143 17.714 258.857c8 20 17.714 34.857 33.143 50.286s30.286 25.143 50.286 33.143c57.714 22.857 194.857 17.714 258.857 17.714s201.143 5.143 258.857-17.714c20-8 34.857-17.714 50.286-33.143s25.143-30.286 33.143-50.286c22.857-57.714 17.714-194.857 17.714-258.857s5.143-201.143-17.714-258.857c-8-20-17.714-34.857-33.143-50.286s-30.286-25.143-50.286-33.143c-57.714-22.857-194.857-17.714-258.857-17.714zM877.714 512c0 60.571 0.571 120.571-2.857 181.143-3.429 70.286-19.429 132.571-70.857 184s-113.714 67.429-184 70.857c-60.571 3.429-120.571 2.857-181.143 2.857s-120.571 0.571-181.143-2.857c-70.286-3.429-132.571-19.429-184-70.857s-67.429-113.714-70.857-184c-3.429-60.571-2.857-120.571-2.857-181.143s-0.571-120.571 2.857-181.143c3.429-70.286 19.429-132.571 70.857-184s113.714-67.429 184-70.857c60.571-3.429 120.571-2.857 181.143-2.857s120.571-0.571 181.143 2.857c70.286 3.429 132.571 19.429 184 70.857s67.429 113.714 70.857 184c3.429 60.571 2.857 120.571 2.857 181.143z"></path>
            </svg>
            <svg viewBox="0 0 602.2582857142856 1024" className="home-icon08">
              <path d="M548 6.857v150.857h-89.714c-70.286 0-83.429 33.714-83.429 82.286v108h167.429l-22.286 169.143h-145.143v433.714h-174.857v-433.714h-145.714v-169.143h145.714v-124.571c0-144.571 88.571-223.429 217.714-223.429 61.714 0 114.857 4.571 130.286 6.857z"></path>
            </svg>
          </div>
        </div>
      </header>
      
      <div className="EmptySpace">

      </div>
      <section className="home-hero">
      <div className="home-heading">
          <h1 className="home-header">Reward your Subordinates</h1>
          <p className="home-caption">
          Digitize your content
          </p>
        </div>
        <div className="home-buttons">
          {/* <button onClick={checkConnectionBeforeConnecting} className="button">
            {connectmsg}
          </button> */}
          
        </div>
      </section>
      <section className="home-description">
      
    
    <div className="home-container">
     <form onSubmit={getBalance}>
        <label className='home-logo'>Get Balance of your wallet</label> <br></br>
         <label className='home-links'style={{color: "white"}}>Wallet Address</label>
         <input type="text" id="walletid" style={{width: 300}} className="button"></input>
         <br></br><br></br>
         <button type="submit" className='home-button6 button'>GetBalance</button>
        
     </form>
     <br>
     </br>
      <form onSubmit={sendMATIC}>
        <label className='home-logo'>Rewarding will only support growth</label> <br></br>
         <label className='home-links'style={{color: "white"}}>Wallet Address</label>
         <input type="text" id="walletaddress" style={{width: 300}} className="button"></input>
         <br></br><br></br>
         <label className='home-links' style={{color: "white"}}>Enter Amount</label>
         <input type="text" id="amount" placeholder="Enter Your Amount" className='home-button7 button'></input>

         <button type="submit" className='home-button6 button'>SEND</button>
        
     </form>
     
    </div>
        <img
          alt="image"
          src="/hero-divider-1500w.png"
          className="home-divider-image"
        />
        
      </section>
      
      <footer className="home-footer">
        <div className="home-main5">
          <div className="home-branding">
            <div className="home-heading10">
              <h2 className="home-logo2">ZKBuilders</h2>
              <p className="home-caption17">
              Empower your professional journey with Autocrate. Join us in creating a job market where trust is inherent, and your identity is truly yours. Let's build a decentralized future together.
              </p>
            </div>
            <div className="home-socials1">
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noreferrer noopener"
                className="home-twitter1 social button"
              >
                <img
                  alt="image"
                  src="/Icons/twitter.svg"
                  className="home-image32"
                />
              </a>
              <a
                href="https://discord.com"
                target="_blank"
                rel="noreferrer noopener"
                className="home-discord1 social button"
              >
                <img
                  alt="image"
                  src="/Icons/discord.svg"
                  className="home-image33"
                />
              </a>
            </div>
          </div>
          <div className="home-links1">
            <div className="home-list1">
              <h3 className="home-heading11">Site</h3>
              <div className="home-items">
                <button className="home-link02 button-clean button">
                  About
                </button>
                <button className="home-link03 button-clean button">
                  Collection
                </button>
                <button className="home-link04 button-clean button">
                  Roadmap
                </button>
                <button className="home-link05 button-clean button">
                  Features
                </button>
              </div>
            </div>
            <div className="home-list2">
              <h3 className="home-heading12">Company</h3>
              <div className="home-items1">
                <button className="home-link06 button-clean button">
                  Team
                </button>
                <button className="home-link07 button-clean button">
                  Press
                </button>
                <button className="home-link08 button-clean button">
                  Terms
                </button>
                <button className="home-link09 button-clean button">
                  Limitations
                </button>
                <button className="home-link10 button-clean button">
                  Licenses
                </button>
              </div>
            </div>
          </div>
          <div className="home-socials2">
            <a
              href="https://twitter.com"
              target="_blank"
              rel="noreferrer noopener"
              className="home-twitter2 social button"
            >
              <img
                alt="image"
                src="/Icons/twitter.svg"
                className="home-image34"
              />
            </a>
            <a
              href="https://discord.com"
              target="_blank"
              rel="noreferrer noopener"
              className="home-discord2 social button"
            >
              <img
                alt="image"
                src="/Icons/discord.svg"
                className="home-image35"
              />
            </a>
          </div>
        </div>
        <span className="home-copyright">
          © 2023 Character. All Rights Reserved.
        </span>
      </footer>
      <div>
        <Script>
          
        </Script>
      </div>
    </div>
  );
};

export default Rewards;
