import React from "react";

function ChatList({ chats, onChatSelect }) {
  const handleSelect = (event) => {
    event.preventDefault();
    console.log(event.target.getAttribute("data-chat-id"));
    onChatSelect(event.target.getAttribute("data-chat-id"));
  };
  return (
    <aside className="menu">
      <p className="menu-label">Chats</p>
      <button
        type="button"
        className="button"
        data-chat-id="new"
        onClick={handleSelect}
      >
        New Chat
      </button>
      <button
        type="button"
        className="button"
        data-chat-id="private"
        onClick={handleSelect}
      >
        New Private Chat
      </button>
      <ul className="menu-list">
        {chats.map((chat) => (
          <li key={chat.id}>
            <a href="#" data-chat-id={chat.id} onClick={handleSelect}>
              {chat.title} <span className="tag">{chat.model}</span>
            </a>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default ChatList;
