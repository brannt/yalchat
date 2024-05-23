export default {
  BACKEND_URL: process.env.REACT_APP_BACKEND_URL || "http://0.0.0.0:8000",
  TELEGRAM_BOT_NAME:
    process.env.REACT_APP_TELEGRAM_BOT_NAME || "helpfulai_login_dev_bot",
  TELEGRAM_REDIRECT_URL:
    process.env.REACT_APP_TELEGRAM_REDIRECT_URL ||
    "http://localhost:8000/auth/telegram/callback",
  DEFAULT_MODEL: process.env.REACT_APP_DEFAULT_MODEL || "ollama_chat/phi3",
};
