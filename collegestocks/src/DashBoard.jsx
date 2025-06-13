import React, { useState, useEffect } from 'react';
import './DashBoard.css';

function StockDashboard({ userId, userName }) {
  const [balance, setBalance] = useState(null);
  const [stocklist, setStocks] = useState({});
  const [error, setError] = useState(null);
  const [portfolio, setPortfolio] = useState();
  const [allStocks, setAllStocks] = useState({});

  // Sanitize stock names to make valid HTML IDs
  const sanitizeId = (name) => name.replace(/[^a-zA-Z0-9_-]/g, "_");

  const fetchBalance = async () => {
    try {
      const res = await fetch(`http://localhost:5000/import?userID=${userId}`);
      const data = await res.json();
      if (res.ok) {
        setBalance(data.balance);
        setStocks(data.stocks);
        setError(null);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError("Server not reachable");
    }
  };

  const fetchAllStocks = async () => {
    try {
      const res = await fetch('http://localhost:5001/get_stocks');
      const data = await res.json();
      if (res.ok) setAllStocks(data);
    } catch (err) {
      console.error("Server not reachable");
    }
  };

  useEffect(() => {
    fetchBalance();
    fetchAllStocks();
  }, [userId]);

  const calculateBalance = (stocklist) => {
    let total = 0;
    for (const [stockName, quantity] of Object.entries(stocklist)) {
      total += quantity * (allStocks[stockName]?.Price || 0);
    }
    return total;
  };

  useEffect(() => {
    const total = calculateBalance(stocklist);
    setPortfolio(total);
  }, [stocklist, allStocks]);

  const availableStocks = Object.entries(allStocks)
    .filter(([stockName]) => (stocklist[stockName] || 0) === 0)
    .map(([_, stock]) => stock);

  const handleBuy = async (stock, price) => {
    const input = document.querySelector(`#inputQuant-${sanitizeId(stock)}`);
    const quantity = input?.value;

    if (!quantity || quantity <= 0) {
      alert("Enter valid quantity");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/buy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userID: userId,
        stockPrice: price,
        quantity: parseInt(quantity),
        stockName: stock,
      }),
    });

    const data = await res.json();
    alert(data.message);
    if (res.ok) {
      fetchBalance();
    }
  };

  const handleSell = async (stock, price) => {
    const input = document.querySelector(`#inputQuant-${sanitizeId(stock)}`);
    const quantity = input?.value;

    if (!quantity || quantity <= 0) {
      alert("Enter valid quantity");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/sell", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userID: userId,
        stockPrice: price,
        quantity: parseInt(quantity),
        stockName: stock,
      }),
    });

    const data = await res.json();
    alert(data.message);
    if (res.ok) {
      fetchBalance();
    }
  };

  return (
    <div className="dash">
      <div className="head"><h1>NITWSE</h1></div>
      <div className="details">
        <div className="name">Hello, {userName}</div>
        
        <div className="balance">Balance : WINT {balance !== null ? balance : 'Loading...'}</div>
      </div>
      <div className="portfolio">
        <div className="portfoliocard">
          <div className="header"><h2>Portfolio:</h2></div>
          <div className="amount"><h3>WINT {portfolio}</h3></div>
        </div>
      </div>
      <div className="stocklistings">
        <div className="list">
          {Object.entries(stocklist)
            .filter(([_, quantity]) => quantity > 0)
            .map(([stockName, quantity], index) => (
              <div className="stock-card" key={index} id={`card-${sanitizeId(stockName)}`}>
                <div className="stock-head">
                  <div className="stock-name">{stockName}</div>
                  <div className="stock-price">WINT {allStocks[stockName]?.Price || "..."}</div>
                </div>
                <div className="stock-owned">Owned: {quantity}</div>
                <div id="input">
                  <input
                    className="quantbox"
                    type="number"
                    min="1"
                    placeholder="Qty"
                    id={`inputQuant-${sanitizeId(stockName)}`}
                  />
                </div>
                <div className="buttons">
                  <button className="buy-btn" onClick={() => handleBuy(stockName, allStocks[stockName]?.Price)}>Buy</button>
                  <button className="sell-btn" onClick={() => handleSell(stockName, allStocks[stockName]?.Price)}>Sell</button>
                </div>
              </div>
            ))}
        </div>
      </div>
      <div className="available">
        <h4>Available Stocks</h4>
      </div>
      <div className="list">
        {availableStocks.map((stock, index) => (
          <div className="stock-card" key={index} id={`card-${sanitizeId(stock.Name)}`}>
            <div className="stock-head">
              <div className="stock-name">{stock.Name}</div>
              <div className="stock-price">WINT {stock.Price}</div>
            </div>
            <div id="input">
              <input
                className="quantbox"
                type="number"
                min="1"
                placeholder="Qty"
                id={`inputQuant-${sanitizeId(stock.Name)}`}
              />
            </div>
            <div className="buttons">
              <button className="buy-btn" onClick={() => handleBuy(stock.Name, stock.Price)}>Buy</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StockDashboard;
