import config from "../config";

async function getCurrentUser() {
  try {
    const response = await fetch(`${config.BACKEND_URL}/api/users/me`, {
      credentials: "include",
    });
    if (!response.ok) {
      return null;
    }
    const user = await response.json();
    return user;
  } catch (err) {
    return null;
  }
}

async function loginUser(username, password) {
  const response = await fetch(`${config.BACKEND_URL}/auth/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  });
  if (!response.ok) {
    throw new Error("Login failed");
  }
}

export { getCurrentUser, loginUser };
