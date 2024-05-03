import logo from './logo.svg';
import './App.css';
import {BACKEND_PATH} from './constants'
import DjangoBridge from './autentication';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a href={BACKEND_PATH+"movies"}>
          {BACKEND_PATH}movies

        </a>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <DjangoBridge/>
      </header>
    </div>
  );
}

export default App;
