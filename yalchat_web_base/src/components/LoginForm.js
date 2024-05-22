import React, { useState } from "react";
import config from "../config";

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const res = await fetch(`${config.BACKEND_URL}/auth/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
        credentials: "include",
      });
      onLoginSuccess();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <section className="section container">
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
        </div>
      </div>
    </section>
  );
}

export default LoginForm;
