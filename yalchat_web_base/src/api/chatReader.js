import config from "../config";
async function privateChatReader(message, history) {
  const response = await fetch(`${config.BACKEND_URL}/api/simple_chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, history }),
  });

  if (!response.body) {
    return;
  }
  let decoder = new TextDecoderStream();
  const reader = response.body.pipeThrough(decoder).getReader();
  return reader;
}

async function chatReader(chatId, message) {
  const response = await fetch(
    `${config.BACKEND_URL}/api/chats/${chatId}/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    }
  );

  if (!response.body) {
    return;
  }
  let decoder = new TextDecoderStream();
  const reader = response.body.pipeThrough(decoder).getReader();
  return reader;
}

async function readChatResponse(reader, setMessagesCallback) {
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

export { privateChatReader, chatReader, readChatResponse };
