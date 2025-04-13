import React, { useState } from 'react';
import axios from 'axios';
import StockRecommendation from './StockRecommendation';

function ThemeCard({ theme }) {
  const [summary, setSummary] = useState('');
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async () => {
    setLoading(true);
    const res = await axios.get(`http://localhost:5000/api/stocks?theme=${encodeURIComponent(theme)}`);
    setSummary(res.data.summary);
    setStocks(res.data.stocks);
    setLoading(false);
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-lg font-semibold">{theme}</h2>
      <button
        onClick={fetchRecommendations}
        className="mt-2 px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded"
      >
        {theme} Stock Recommendations
      </button>
      {loading && <p>Loading...</p>}
      {summary && <p className="mt-2 italic">{summary}</p>}
      <div className="mt-4 grid grid-cols-1 gap-2">
        {stocks.map(stock => (
          <StockRecommendation key={stock.ticker} stock={stock} />
        ))}
      </div>
    </div>
  );
}

export default ThemeCard;