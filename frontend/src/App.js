// import Analysis from "./Analysis";
import "./App.css";
import Analysis from "./Analysis";
import UserAuth from "./UserAuth";
import axios from "axios";

import React, { useState } from "react";

const baseURL = "http://127.0.0.1:8000/";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

axios.defaults.withCredentials = true;

const getCookie = (name) => {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="))
    ?.split("=")[1];
  return cookieValue;
};

const csrfToken = getCookie("csrftoken");

const client = axios.create({
  baseURL: baseURL,
  headers: {
    "X-CSRFToken": csrfToken,
  },
});

const fetchCsrfToken = async () => {
  try {
    await axios.get(`${baseURL}api/csrf/`);
    console.log("CSRF token set successfully");
  } catch (error) {
    console.error(
      "Error setting CSRF token:",
      error.response?.data || error.message
    );
  }
};

const App = () => {
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState();
  // const [registrationToggle, setRegistrationToggle] = useState(false);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  // console.log("is logged in: ", isLoggedIn);

  function submitLogout(e) {
    // e.preventDefault();
    client.post("/logout/", { withCredentials: true }).then(function (res) {
      setCurrentUser(false);
      setEmail("");
      setUsername("");
    });
  }

  const handleButtonClick = () => {
    if (isLoggedIn) {
      // Handle logout
      setIsLoggedIn(false);
      submitLogout();
    } else {
      // Toggle between login and registration
      setRegistrationToggle(!registrationToggle);
    }
  };

  const getButtonLabel = () => {
    if (isLoggedIn) return "Logout";
    return registrationToggle ? "Login" : "Register";
  };

  return (
    <div>
      {/* Floating Button */}
      <button className="floating-button" onClick={handleButtonClick}>
        {getButtonLabel()}
      </button>
      {isLoggedIn ? (
        // Show the main app if the user is logged in
        <Analysis />
      ) : (
        // Show the authentication forms if the user is not logged in
        <UserAuth
          registrationToggle={registrationToggle}
          setRegistrationToggle={setRegistrationToggle}
          setIsLoggedIn={setIsLoggedIn} // Pass login state updater
          fetchCsrfToken={fetchCsrfToken}
          client={client}
          currentUser={currentUser}
          setCurrentUser={setCurrentUser}
          email={email}
          setEmail={setEmail}
          username={username}
          setUsername={setUsername}
        />
      )}
    </div>
  );
};

export default App;
