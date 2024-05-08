# Yet Another LLM Chat project

This is a simple ChatGPT-like UI for communicating with arbitrary LLMs. The backend is a FastAPI server that manages the chats and wraps the LLM calls (with `litellm`, so all LLMs supported by it are supported here).
The frontend is a simple React app that sends the messages to the backend and displays the responses.

## Roadmap

- [x] Basic chat functionality
- [x] Basic chat storage and management
- [ ] Fix issues
  - [ ] Chats no loading
- [ ] Add cloud LLMs
- [ ] Login with OAuth
- [ ] Deploy
- [ ] Add model management (list user models, add API keys, select from UI)
