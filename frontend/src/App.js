import axios from "axios";
import React, { useEffect, useState, useContext } from "react";
import { format } from "date-fns";
import "./App.css";
import { Line } from "react-chartjs-2";
import Chart from 'chart.js/auto';
import 'chartjs-adapter-moment';


const baseUrl = "http://localhost:8000/api";
// const Context = React.createContext(null);

// const LoginModal = () => {
//   // const { store, actions } = useContext(Context);
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const token = sessionStorage.getItem("token");

  // const handleLogin = async () => {
  //   try {
  //     const dt = {
  //       email: "test",
  //       password: "test",
  //     };
  //     const resp = await axios.post(`${baseUrl}/token`, dt);
  //     console.log("dt: ", dt);
  //     console.log("resp: ", resp);
  //     if (resp.status === 200) {
  //       sessionStorage.setItem("token", resp.data.access_token);
  //       return resp;
  //     } else alert("There was an error");
  //   } catch {
  //     console.log("login error");
  //   }
  // };

  // const handleLogout = () => {
  //   sessionStorage.setItem("token", "");
  // };

//   return (
//     <div>
//       <h1>Login</h1>
//       <div>
//         {token && token !== "" && token !== "undefined" ? (
//           <div>You are logged in</div>
//         ) : (
//           <div>
//             <input
//               type="text"
//               placeholder="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//             />
//             <input
//               type="password"
//               placeholder="password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//             />
//             <button onClick={handleLogin}>Login</button>
//           </div>
//         )}
//       </div>
//       <button onClick={handleLogout}>Logout</button>
//     </div>
//   );
// };

function App() {
  const [description, setDescription] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [eventsList, setEventsList] = useState([]);
  const [eventIdBeingEdited, setEventIdBeingEdited] = useState(null); // id of event currently being edited

  const fetchEvents = async () => {
    // console.log("fetching events");
    const resp = await axios.get(`${baseUrl}/entries/`);
    // console.log("data: ", resp.data, typeof(resp.data));
    const events = resp.data;
    console.log("events: ", events, typeof(events));
    // console.log("emotions: ", events[9]?.emotions[0][15]);
    // console.log("emotions map: ", events?.map(event => event?.emotions[0][15].score));
    setEventsList(events);
  };

  const handleChange = (e, field) => {
    setDescription(e.target.value);
  };

  const handleEditChange = (e, field) => {
    setEditDescription(e.target.value);
  };

  const handleDelete = async (event) => {
    const id = event.id;
    try {
      await axios.delete(`${baseUrl}/entries/${id}/`);
      const updatedList = eventsList.filter((event) => event.id !== id);
      setEventsList(updatedList);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleEdit = (event) => {
    setEventIdBeingEdited(event.id);
    console.log("setting event id being edited:", event.id);
    setEditDescription(event.description);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault(); //prevents page from refreshing
    try {
      const url = `${baseUrl}/entries/${eventIdBeingEdited}/`;
      console.log(url);
      const data = await axios.put(url, { description: editDescription });
      // console.log(editDescription);
      const updatedEvent = data.data.event;
      const updatedlist = eventsList.map((event) => {
        if (event.id === eventIdBeingEdited) {
          return (event = updatedEvent);
        }
        return event;
      });
      setEventsList(updatedlist);
      setDescription("");
      setEventIdBeingEdited(null);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleCancelEdit = () => {
    setEditDescription("");
    setEventIdBeingEdited(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); //prevents page from refreshing
    try {
      console.log(`${baseUrl}/entries/`, { description });
      const data = await axios.post(`${baseUrl}/entries/`, { "description" : description });
      setEventsList([...eventsList, data.data]);
      setDescription("");
    } catch (err) {
      console.error(err.message);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const emotions = ["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise"];
  const default_emotions_dict = {};
  emotions.map(emotion => default_emotions_dict[emotion] = false);
  const [checked, setChecked] = React.useState(default_emotions_dict);

  const checked_emotions = emotions.filter(emotion => checked[emotion]);
  
  // TODO: get correct data for each emotion
  const datasets = checked_emotions.map(emotion =>
      ({
        label: emotion,
        data: eventsList.map(event => event.emotions[0][emotions.indexOf(emotion)].score),
        fill: true,
        backgroundColor: "rgba(75,192,192,0.2)",
        borderColor: "rgba(75,192,192,1)",
      }));

  datasets.push({
    label: "Composite Sentiment",
    data: eventsList.map(event => event.sentiment),
    fill: true,
    backgroundColor: "rgba(75,192,192,0.2)",
    borderColor: "rgba(75,192,192,1)",
    visible: true
  })
                                  
  
  const handleCheckboxChange = (emotion) => 
  {
    setChecked(prevChecked => ({...prevChecked, [emotion]: !prevChecked[emotion]}));
  }


  // {
  //   label: "Gratitude",
  //   data: eventsList.map(event => event.emotions[0][15].score),
  //   fill: true,
  //   backgroundColor: "rgba(75,192,192,0.2)",
  //   borderColor: "rgba(75,192,192,1)"
  // }

  const datasets_old = [
    {
      label: "Composite Sentiment",
      data: eventsList.map(event => event.sentiment),
      fill: true,
      backgroundColor: "rgba(75,192,192,0.2)",
      borderColor: "rgba(75,192,192,1)",
      visible: true
    },
    {
      label: "Gratitude",
      data: eventsList.map(event => event.emotions[0][15].score),
      fill: true,
      backgroundColor: "rgba(75,192,192,0.2)",
      borderColor: "rgba(75,192,192,1)"
    }
  ];

  const eventsData = {
    labels: eventsList.map((event) => event.created_at),
    datasets: datasets,
  };

  // const chartOptions = {
  //   scales: {
  //       x: {
  //         type: 'time',
  //         time: {
  //             unit: 'minute'
  //         }
  //       }
  //   }
  // };

  // const data = {
  //   labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  //   datasets: [
  //     {
  //       label: "First dataset",
  //       data: [33, 53, 85, 41, 44, 65],
  //       fill: true,
  //       backgroundColor: "rgba(75,192,192,0.2)",
  //       borderColor: "rgba(75,192,192,1)"
  //     },
  //     {
  //       label: "Second dataset",
  //       data: [33, 25, 35, 51, 54, 76],
  //       fill: false,
  //       borderColor: "#742774"
  //     }
  //   ]
  // };

  return (
    <div className="App">
      <section>
        <form onSubmit={handleSubmit}>
          <label htmlFor="description">Description</label>
          <input
            onChange={(e) => handleChange(e, "description")}
            type="text"
            name="description"
            id="description"
            value={description}
          />
          <button type="Submit">Submit</button>
        </form>
      </section>
      <Line data={eventsData}
      // options={chartOptions}
      />
       <div>
      {checked_emotions}
      {emotions.map((emotion) => <div>
          <input type="checkbox"
            checked={checked[emotion]}
            onChange={() => handleCheckboxChange(emotion)}
           >
           </input>
                      <div>{emotion}</div>
                      {/* <div>{checked[emotion].toString()}</div> */}
    </div>)}
    </div>
      <section>
        <ul>
          {eventsList.map((event) => {
            return (
              <li key={event.id}>
                {eventIdBeingEdited === event.id ? (
                  <form onSubmit={handleEditSubmit} key={event.id}>
                    <input
                      onChange={(e) => handleEditChange(e, "edit")}
                      type="text"
                      name="editDescription"
                      id="editDescription"
                      value={editDescription}
                    ></input>
                    <button type="Submit">Finish Editing</button>
                    <button type="button" onClick={handleCancelEdit}>
                      Cancel
                    </button>
                  </form>
                ) : (
                  <div>
                    <button onClick={() => handleDelete(event)}>X</button>
                    <button onClick={() => handleEdit(event)}>Edit</button>
                    {format(new Date(event.created_at), "MM/dd/yyyy, p")}:{" "}
                    <br />
                    {event.description}
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </section>
    </div>
  );
}


export default App;
