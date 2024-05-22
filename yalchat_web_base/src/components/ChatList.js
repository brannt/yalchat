import React from "react";
import BeatLoader from "react-spinners/BeatLoader";

function ChatList({ chats, isChatsLoading, onChatSelect }) {
  const handleSelect = (event) => {
    event.preventDefault();
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
      {isChatsLoading ? (
        <div className="container is-flex is-justify-content-center pt-3">
          <BeatLoader color={"#000000"} loading={true} />
        </div>
      ) : (
        <ul className="menu-list">
          {chats.map((chat) => (
            <li key={chat.id}>
              <a href="#" data-chat-id={chat.id} onClick={handleSelect}>
                {chat.title} <span className="tag">{chat.model}</span>
              </a>
            </li>
          ))}
        </ul>
      )}
    </aside>
  );
}

export default ChatList;
