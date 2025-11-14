import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MoodEntry from './pages/MoodEntry';
import AgentProcessing from './pages/AgentProcessing';
import MatchResult from './pages/MatchResult';
import CrisisAlert from './pages/CrisisAlert';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MoodEntry />} />
        <Route path="/processing" element={<AgentProcessing />} />
        <Route path="/match" element={<MatchResult />} />
        <Route path="/crisis" element={<CrisisAlert />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

