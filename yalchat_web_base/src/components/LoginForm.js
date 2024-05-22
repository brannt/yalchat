import React, { useEffect, useState } from "react";
import config from "../config";
import HashLoader from "react-spinners/HashLoader";
import { getCurrentUser, loginUser } from "../api/users";
function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const user = await getCurrentUser();
      user ? onLoginSuccess() : setIsLoading(false);
    })();
  }, []);

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
          </div>
        </div>
      )}
    </section>
  );
}

export default LoginForm;
