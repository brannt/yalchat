import { useState } from "react";
import ChatInterface from "./components/ChatInterface";
import LoginForm from "./components/LoginForm";
import "./App.css";
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div className="App container is-flex is-flex-direction-column">
      <section className="hero is-small">
        <div className="hero-body">
          <div className="container">
            <h1 className="title">
              Helpful Chat, <span className="lol">lol</span>
            </h1>
            <h2 className="subtitle">by brannt</h2>
          </div>
        </div>
      </section>
      {isLoggedIn ? (
        <ChatInterface />
      ) : (
        <LoginForm onLoginSuccess={() => setIsLoggedIn(true)} />
      )}
      <footer className="footer py-6">
        <a target="_blank" href="https://icons8.com/icon/n2XDIOJc6t91/chat">
          Chat
        </a>
        ,{" "}
        <a target="_blank" href="https://icons8.com/icon/60700/sent">
          Send
        </a>
        ,{" "}
        <a target="_blank" href="https://icons8.com/icon/91467/stop-circled">
          Stop
        </a>{" "}
        icons by{" "}
        <a target="_blank" href="https://icons8.com">
          Icons8
        </a>
      </footer>
    </div>
  );
}

export default App;
