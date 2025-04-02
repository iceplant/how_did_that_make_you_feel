// import Analysis from "./Analysis";
import './App.css';
import Analysis from "./Analysis";
import UserAuth from "./UserAuth";
import axios from "axios";

import React, { useState } from "react";

const App = () => {
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  // console.log("is logged in: ", isLoggedIn);

  const handleButtonClick = () => {
    if (isLoggedIn) {
      // Handle logout
      setIsLoggedIn(false);
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
        />
      )}
    </div>
  )
}

export default App;