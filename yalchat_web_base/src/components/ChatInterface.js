import React, { useState, useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import { ROLE } from "../constants";
import "./ChatInterface.css";
import SendIcon from "./icons8-send-30.png";
import StopIcon from "./icons8-stop-30.png";

function fetchChatbotReader(body) {
  const response = fetch("http://localhost:5005/webhooks/rest/webhook", {
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
  return reader;
}

async function readChatbotResponse(reader, setMessagesCallback) {
  let accumulatedAnswer = "";

  while (true) {
    let { value, done } = await reader.read();
    if (done) {
      break;
    }
    accumulatedAnswer += value;
    setMessagesCallback((currentMessages) => {
      const newMessages = [...currentMessages];
      newMessages[newMessages.length - 1].content = accumulatedAnswer;
      return newMessages;
    });
  }
}

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isResponseInProgress, setIsResponseInProgress] = useState(false);
  const [reader, setReader] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
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
    setIsResponseInProgress(true);

    try {
      const reader = await fetchChatbotReader(body);
      if (!reader) {
        return;
      }

      setReader(reader);
      await readChatbotResponse(reader, setMessages);
    } catch (error) {
      console.error(error);
      setError({ message: error, level: "is-danger" });
    } finally {
      setIsResponseInProgress(false);
      setReader(null);
    }
  };

  const handleStop = () => {
    if (reader) {
      reader.cancel();
    }
    setIsResponseInProgress(false);
    setError({ message: "The request was cancelled", level: "is-warning" });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isResponseInProgress) {
      handleSendMessage();
    } else {
      handleStop();
    }
  };

  const enterSumbit = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !isResponseInProgress) {
      e.preventDefault();
      e.target.form.requestSubmit();
    }
  };

  return (
    <article className="message container is-flex is-flex-direction-column">
      <header className="message-header">Chat</header>
      <div className="message-body container is-flex is-flex-direction-column">
        {messages && messages.length === 0 ? (
          <div className="has-text-centered title mt-5">
            <p className="initial-message">Hello! How can I help you today?</p>
          </div>
        ) : null}
        <div className="content is-flex-grow-1 is-flex is-flex-direction-column">
          {messages &&
            messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}
          <div ref={messagesEndRef} />
        </div>

        <div>
          <form onSubmit={handleSubmit}>
            <div className="field is-grouped">
              <div className="control is-expanded">
                <textarea
                  className="textarea pr-6"
                  placeholder="Type a message..."
                  rows="2"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={enterSumbit}
                />
              </div>

              <div className="control is-relative">
                <button type="submit" className="button send-button">
                  <span class="icon">
                    {isResponseInProgress ? (
                      <img
                        src={StopIcon}
                        alt="Stop"
                        height="30px"
                        width="30px"
                      />
                    ) : (
                      <img
                        src={SendIcon}
                        alt="Send"
                        height="30px"
                        width="30px"
                      />
                    )}
                  </span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
      {error && (
        <div className={`notification ${error.level}`}>
          <button className="delete" onClick={() => setError(null)}></button>
          {error.message}
        </div>
      )}
    </article>
  );
}

export default ChatInterface;
