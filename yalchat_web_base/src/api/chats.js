import config from "../config";
async function getChats() {
  const response = await fetch(`${config.BACKEND_URL}/api/chats/`);
  const chats = await response.json();
  return chats;
}

async function getChat(chatId) {
  const response = await fetch(`${config.BACKEND_URL}/api/chats/${chatId}`);
  const chat = await response.json();
  return chat;
}

async function createChat(model, firstMessage) {
  const response = await fetch(`${config.BACKEND_URL}/api/chats/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model, first_message: firstMessage }),
  });
  const chat = await response.json();
  return chat;
}

async function deleteChat(chatId) {
  await fetch(`${config.BACKEND_URL}/api/chats/${chatId}`, {
    method: "DELETE",
  });
}

export { getChats, getChat, createChat, deleteChat };
