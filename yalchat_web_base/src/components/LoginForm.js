import React, { useEffect, useState, useRef } from "react";
import config from "../config";

import HashLoader from "react-spinners/HashLoader";
import { getCurrentUser, loginUser } from "../api/users";

function TelegramLoginButton({ botName, redirectUrl }) {
  const telegramWrapperRef = useRef(null);

  useEffect(() => {
    const scriptElement = document.createElement("script");
    scriptElement.src = "https://telegram.org/js/telegram-widget.js?22";
    scriptElement.setAttribute("data-telegram-login", botName);
    scriptElement.setAttribute("data-size", "large");
    scriptElement.setAttribute("data-auth-url", redirectUrl);
    scriptElement.async = true;

    telegramWrapperRef.current.appendChild(scriptElement);
  }, []);

  return (
    <>
      <div ref={telegramWrapperRef}></div>
    </>
  );
}
function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const user = await getCurrentUser();
      user ? onLoginSuccess() : setIsLoading(false);
    })();
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    try {
      await loginUser(username, password);
      onLoginSuccess();
    } catch (err) {
      // TODO: Show error message
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAuthLogin = async (provider) => {
    const response = await fetch(
      `${config.BACKEND_URL}/auth/${provider}/login`
    );
    const data = await response.json();
    window.location.href = data.oauth.url;
  };

  return (
    <section className="section container">
      {isLoading ? (
        <div
          className="container is-flex is-flex-direction-column is-justify-content-center is-align-items-center"
          style={{ height: "100%" }}
        >
          <HashLoader color={"#000000"} loading={isLoading} size={150} />
        </div>
      ) : (
        <div className="columns is-centered">
          <div className="column is-half">
            <form onSubmit={handleSubmit}>
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                  />
                </div>
              </div>

              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                  />
                </div>
              </div>

              <div className="field">
                <div className="control">
                  <button className="button is-primary" type="submit">
                    Login
                  </button>
                </div>
              </div>
            </form>

            <button
              className="button is-info"
              onClick={() => handleAuthLogin("github")}
            >
              Login with GitHub
            </button>
            <TelegramLoginButton
              botName={config.TELEGRAM_BOT_NAME}
              redirectUrl={config.TELEGRAM_REDIRECT_URL}
            />
          </div>
        </div>
      )}
    </section>
  );
}

export default LoginForm;
