import React from 'react';

const getColor = (recommendation) => {
  switch (recommendation) {
    case 'Strong Buy': return 'bg-green-500';
    case 'Buy': return 'bg-green-300';
    case 'Hold': return 'bg-yellow-300';
    case 'Sell': return 'bg-red-300';
    case 'Strong Sell': return 'bg-red-600';
    default: return 'bg-gray-200';
  }
};

function StockRecommendation({ stock }) {
  return (
    <div className="flex justify-between items-center p-2 border rounded">
      <span>{stock.name} ({stock.ticker})</span>
      <span className={`px-3 py-1 rounded text-white ${getColor(stock.recommendation)}`}>
        {stock.recommendation}
      </span>
    </div>
  );
}

export default StockRecommendation;