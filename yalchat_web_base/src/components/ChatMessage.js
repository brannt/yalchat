import React from "react";
import ReactMarkdown from "react-markdown";
import { ROLE } from "../constants";
function isBotMessage(message) {
  return message.role !== ROLE.USER;
}

function ChatMessage({ message }) {
  const isBot = isBotMessage(message);
  const content = isBot ? (
    <ReactMarkdown children={message.content} />
  ) : (
    message.content
  );

  return (
    <div
      className={`chat-message box ${isBot ? "bot-message" : "user-message"}`}
    >
      <p>
        <strong>{isBot ? "Bot:" : "User:"}</strong>
      </p>
      <p>{content}</p>
    </div>
  );
}

export default ChatMessage;
