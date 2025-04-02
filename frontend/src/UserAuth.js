import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

axios.defaults.withCredentials = true;

// const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

const getCookie = (name) => {
  const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith(name + '='))
      ?.split('=')[1];
  return cookieValue;
};
const csrfToken = getCookie('csrftoken');

const baseURL = "http://127.0.0.1:8000/";

const client = axios.create({
  baseURL: baseURL,
  headers: {
    'X-CSRFToken': csrfToken
  }
})

const fetchCsrfToken = async () => {
  try {
    await axios.get(`${baseURL}api/csrf/`);
    console.log("CSRF token set successfully");
  } catch (error) {
    console.error("Error setting CSRF token:", error.response?.data || error.message);
  }
};

const UserAuth = ({ registrationToggle, setRegistrationToggle, setIsLoggedIn }) => {
  const [currentUser, setCurrentUser] = useState();
  // const [registrationToggle, setRegistrationToggle] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    fetchCsrfToken();
    client.get("/user/")
    .then(function(res) {
      // console.log("user response: ", res);
      setCurrentUser(true);
      setEmail(res.data.user.email);
      setUsername(res.data.user.username);
      // console.log(res);
    })
    .catch(function(error) {
      setCurrentUser(false);
    });
  }, []);

  function update_form_btn() {
    if (registrationToggle) {
      document.getElementById("form_btn").innerHTML = "Register";
      setRegistrationToggle(false);
    } else {
      document.getElementById("form_btn").innerHTML = "Log in";
      setRegistrationToggle(true);
    }
  }

  function submitRegistration(e) {
    e.preventDefault();
    client.post(
      "/register/",
      {
        email: email,
        username: username,
        password: password
      }
    ).then(function(res) {
      client.post(
        "/login/",
        {
          email: email,
          password: password
        }
      ).then(function(res) {
        setCurrentUser(true);
        setEmail(email);
        setUsername(username);
        setIsLoggedIn(true);
      });
    });
  }

  function submitLogin(e) {
    e.preventDefault();
    client.post(
      "/login/",
      {
        email: email,
        password: password
      }
    ).then(function(res) {
      console.log(res);
      setCurrentUser(true);
      setEmail(email);
      setUsername(username);
      setIsLoggedIn(true);
    });
  }

  function submitLogout(e) {
    e.preventDefault();
    client.post(
      "/logout/",
      {withCredentials: true}
    ).then(function(res) {
      setCurrentUser(false);
      setEmail("");
      setUsername("");
    });
  }

  if (currentUser) {
    return (
      <div className="center vertical-align">
        <Navbar bg="dark" variant="dark">
          <Container>
            {/* <Navbar.Brand></Navbar.Brand> */}
            {/* <Navbar.Toggle /> */}
            <Navbar.Collapse className="justify-content-end">
              <div className="navbar-content">
                <div className="logged-in-info">
                  <h2>You're logged in!</h2>
                  <h3>email: {email}</h3>
                  <h3>username: {username}</h3>
                </div>
                <form onSubmit={(e) => submitLogout(e)}>
                  <Button type="submit" variant="light">Log out</Button>
                </form>
              </div>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        </div>
    );
  }
  return (
    <div>
    {
      registrationToggle ? (
        <div className="center">
          <Form onSubmit={e => submitRegistration(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
              <Form.Text className="text-muted">
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>        
      ) : (
        <div className="center">
          <Form onSubmit={e => submitLogin(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
              <Form.Text className="text-muted">
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>
      )
    }
    <Navbar bg="dark" variant="dark">
      <Container>
        {/* <Navbar.Brand>Authentication App</Navbar.Brand> */}
        {/* <Navbar.Toggle /> */}
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            <Button id="form_btn" onClick={update_form_btn} variant="light">Register</Button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    </div>
  );
}

export default UserAuth;