import React, { useState } from 'react';
import axios from 'axios';
import ThemeCard from './components/ThemeCard';

function App() {
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState(false);

  const fetchThemes = async () => {
    setLoading(true);
    const response = await axios.get('http://localhost:5000/api/themes');
    setThemes(response.data);
    setGenerated(true);
    setLoading(false);
  };

  const reset = () => {
    setThemes([]);
    setGenerated(false);
  };

  return (
    <div className="p-8">
      <button
        onClick={generated ? reset : fetchThemes}
        className="px-4 py-2 bg-blue-500 text-white rounded shadow"
      >
        {generated ? 'Regenerate Schwab Themes' : 'Generate Schwab Themes'}
      </button>

      <div className="mt-6 space-y-4">
        {themes.map(theme => (
          <ThemeCard key={theme} theme={theme} />
        ))}
      </div>
    </div>
  );
}

export default App;