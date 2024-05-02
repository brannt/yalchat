import React, { useState, useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import { ROLE } from "../constants";
import "./ChatInterface.css";
import PaperPlane from "./icons8-send-30.png";

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async (event) => {
    event.preventDefault();

    if (!inputText.trim()) {
      return;
    }

    const userMessage = { content: inputText, role: ROLE.USER };
    const body = {
      history: [...messages, userMessage],
      query: inputText,
    };
    const botMessage = { content: "", role: ROLE.ASSISTANT };
    setMessages([...body.history, botMessage]);
    setInputText("");

    const response = await fetch("http://localhost:8000/api/stream_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!response.body) {
      return;
    }

    let decoder = new TextDecoderStream();
    const reader = response.body.pipeThrough(decoder).getReader();
    let accumulatedAnswer = "";

    while (true) {
      let { value, done } = await reader.read();
      if (done) {
        break;
      }
      accumulatedAnswer += value;
      setMessages((currentMessages) => {
        const newMessages = [...currentMessages];
        newMessages[newMessages.length - 1].content = accumulatedAnswer;
        return newMessages;
      });
    }
  };

  const enterSumbit = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      console.log("Enter key pressed");
      e.target.form.requestSubmit();
    }
  };

  return (
    <article className="message container is-flex is-flex-direction-column">
      <header className="message-header">Chat</header>
      <div className="message-body container is-flex is-flex-direction-column">
        {messages && messages.length === 0 ? (
          <nav className="level is-flex-grow-1">
            <div className="level-item has-text-centered is-align-content-center title">
              <p className="initial-message">
                Hello! How can I help you today?
              </p>
            </div>
          </nav>
        ) : null}
        <div className="content is-flex-grow-1 is-flex is-flex-direction-column">
          {messages &&
            messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}
          <div ref={messagesEndRef} />
        </div>

        <div>
          <form onSubmit={handleSendMessage}>
            <div className="field">
              <div className="control">
                <textarea
                  className="textarea"
                  placeholder="Type a message..."
                  rows="2"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={enterSumbit}
                />
              </div>
            </div>
            <div className="field">
              <div className="control">
                <button type="submit" className="button">
                  <span class="icon">
                    <img
                      src={PaperPlane}
                      alt="Send"
                      height="30px"
                      width="30px"
                    />
                  </span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </article>
  );
}

export default ChatInterface;
