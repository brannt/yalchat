import { logoutUser } from "../api/users";
import "./NavBar.css";

function NavBar({ isLoggedIn, onLogOut }) {
  const handleSignOut = async () => {
    await logoutUser();
    onLogOut();
  };

  return (
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <div className="p-3 pl-5">
          <h1 className="title">
            Helpful Chat, <span className="lol">lol</span>
          </h1>
          <h2 className="subtitle">
            <sup>by brannt</sup>
          </h2>
        </div>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <div class="navbar-item">
            {isLoggedIn && (
              <button className="button is-light mr-2" onClick={handleSignOut}>
                Sign Out
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
