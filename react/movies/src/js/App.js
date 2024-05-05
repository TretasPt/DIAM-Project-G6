import '../css/App.css';
import Autentication from './Autentication';
import Feature from './Feature';
import { useState } from 'react';

function App() {

  const [username, setUsername] = useState('');
  const [isAutenticated, setIsAutenticated] = useState(false);


  return (
    <div className="App">
      <header className="App-header">
        <Autentication setUsername={setUsername} isAutenticated={isAutenticated} setIsAutenticated={setIsAutenticated} username={username} />
        <Feature username={username}/>
      </header>
    </div>
  );
}

export default App;
