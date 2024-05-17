import React, { useState, useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import { ROLE } from "../constants";
import {
  chatReader,
  privateChatReader,
  readChatResponse,
} from "../api/chatReader";
import { createChat, getChat } from "../api/chats";

import "./Chat.css";
import SendIcon from "./icons8-send-30.png";
import StopIcon from "./icons8-stop-30.png";
import config from "../config";

function Chat({ chatId, onNewChat }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [chatMetadata, setChatMetadata] = useState({
    title: "",
    model: "",
    tags: [],
  });
  const [isResponseInProgress, setIsResponseInProgress] = useState(false);
  const [reader, setReader] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  useEffect(() => {
    if (chatId && chatId !== "new" && chatId !== "private") {
      (async () => {
        const chat = await getChat(chatId);
        setMessages(chat.history);
        setChatMetadata({
          title: chat.title,
          model: chat.model,
          tags: chat.tags,
        });
      })();
    } else {
      setMessages([]);
      setChatMetadata({
        title: "New Chat",
        model: config.DEFAULT_MODEL,
        tags: chatId === "private" ? ["private"] : [],
      });
    }
  }, [chatId]);

  const scrollToBottom = () => {
    if (isResponseInProgress) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) {
      return;
    }

    const userMessage = { content: inputText, role: ROLE.USER };
    const botMessage = { content: "", role: ROLE.ASSISTANT };
    setMessages([...messages, userMessage, botMessage]);
    setInputText("");
    setIsResponseInProgress(true);

    try {
      if (!chatId || chatId === "new") {
        const newChat = await createChat(config.DEFAULT_MODEL, inputText);
        setChatMetadata({
          title: newChat.title,
          model: newChat.model,
          tags: newChat.tags,
        });
        if (onNewChat) {
          onNewChat(newChat.id);
        }
        chatId = newChat.id;
      }
      let reader;
      if (chatId === "private") {
        reader = await privateChatReader(inputText, messages);
      } else {
        reader = await chatReader(chatId, inputText);
      }
      if (!reader) {
        return;
      }

      setReader(reader);
      await readChatResponse(reader, setMessages);
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
      <header className="message-header">
        <p>{chatMetadata.title}</p>
        <ul>
          <li style={{ display: "inline" }} class="mr-1">
            <span class="tag">{chatMetadata.model}</span>
          </li>
          {chatMetadata.tags.map((tag) => (
            <li key={tag} style={{ display: "inline" }} class="mr-1">
              <span class="tag">{tag}</span>
            </li>
          ))}
        </ul>
      </header>

      <div className="message-body container is-flex is-flex-direction-column">
        {messages && messages.length === 0 ? (
          <div className="has-text-centered title mt-5">
            <p className="initial-message">Hello! How can I help you today?</p>
          </div>
        ) : null}
        <div className="content is-flex-grow-1 is-flex is-flex-direction-column">
          <div
            className={`message-list ${
              isResponseInProgress ? "is-writing" : ""
            }`}
          >
            {messages &&
              messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
          </div>
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
                  <span className="icon">
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
          {JSON.stringify(error)}
        </div>
      )}
    </article>
  );
}

export default Chat;
