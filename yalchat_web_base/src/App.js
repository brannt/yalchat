import ChatInterface from "./components/ChatInterface";
function App() {
  return (
    <div className="App container is-flex is-flex-direction-column">
      <section className="hero is-small is-info">
        <div className="hero-body">
          <div className="container">
            <h1 className="title">Yet Another LLM Chat App</h1>
            <h2 className="subtitle">A humble chatbot</h2>
          </div>
        </div>
      </section>
      <ChatInterface />
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
