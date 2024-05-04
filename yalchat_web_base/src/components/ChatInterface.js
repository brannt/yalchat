import React, { useState, useEffect } from "react";
import Chat from "./Chat";
import ChatList from "./ChatList";
import { getChats } from "../api/chats";

function ChatInterface() {
  const [chats, setChats] = useState([]);
  const [chatId, setChatId] = useState(null);
  const [reloadChats, setReloadChats] = useState(true);

  useEffect(() => {
    if (!reloadChats) {
      return;
    }
    (async () => {
      const chats = await getChats();
      setChats(chats);
      setReloadChats(false);
    })();
  }, []);
  return (
    <section className="section container is-flex">
      <div className="columns container">
        <div className="column is-one-quarter">
          <ChatList chats={chats} onChatSelect={(id) => setChatId(id)} />
        </div>

        <div className="container is-max-desktop is-flex is-flex-direction-column">
          <Chat chatId={chatId} onNewChat={() => setReloadChats(true)} />
        </div>
      </div>
    </section>
  );
}

export default ChatInterface;
