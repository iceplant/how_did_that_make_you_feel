import axios from "axios";
import React, { useEffect, useState, useContext } from "react";
import { format } from "date-fns";
// import "./App.css";
import { Line } from "react-chartjs-2";
import Chart from 'chart.js/auto';
import 'chartjs-adapter-moment';
import styles from "./App.module.css"


const baseUrl = "http://localhost:8000/api";


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
  emotions.map(emotion => default_emotions_dict[emotion] = true);
  const [checked, setChecked] = React.useState(default_emotions_dict);

  const checked_emotions = emotions.filter(emotion => checked[emotion]);
  
  const rbgaClear = "rgba(0,0,0,0)"

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
    backgroundColor: rbgaClear,
    borderColor: "rgba(200,192,192,1)",
    visible: true
  })

  datasets.push({
    label: "TextBlob Polarity",
    data: eventsList.map(event => event.blob_sentiment[0]),
    fill: true,
    backgroundColor: rbgaClear,
    borderColor: "rgba(19, 157, 180, 0.8)",
    visible: true
  })

  datasets.push({
    label: "TextBlob Subjectivity",
    data: eventsList.map(event => event.blob_sentiment[1]),
    fill: true,
    backgroundColor: rbgaClear,
    borderColor: "rgba(245, 40, 145, 0.8)",
    visible: true
  })
                                  
  
  const handleCheckboxChange = (emotion) => 
  {
    setChecked(prevChecked => ({...prevChecked, [emotion]: !prevChecked[emotion]}));
  }

  const eventsData = {
    labels: eventsList.map((event) => event.created_at),
    datasets: datasets,
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Analysis'
      }
    },
    scales: {
      x: {
        type: 'time',
        time: {
            unit: 'hour', // Change to 'minute', 'hour', etc. as needed
            tooltipFormat: 'll HH:mm', // Format for tooltip display
            displayFormats: {
                day: 'MMM D', // Format for day-level labels
                hour: 'MMM D, HH:mm' // Format for hour-level labels
            }
        },
        title: {
            display: true,
            text: 'Date and Time'
        },
        ticks: {
            // Customize tick labels if needed
            callback: function(value) {
                const date = new Date(value);
                return date.toLocaleString(); // Custom format using toLocaleString() if needed
            }
        }
    },
      y: {
        display: true,
        // beginAtZero: true,
        // type: 'logarithmic',
      }
    }
  };

  return (
    <div className="App">
      <h2>How are you doing today? What happened? How did that make you feel?</h2>
      <section>
        <form onSubmit={handleSubmit}>
          <label htmlFor="description"></label>
          <textarea
            className={styles.text_box}
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
      options={chartOptions}
      />
       <div className={styles.emotions_checkboxes}>
      {emotions.map((emotion) => <div>
          <input type="checkbox" key={emotion}
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
