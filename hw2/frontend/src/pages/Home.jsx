import { useState, useEffect } from 'react'
import api from '../api'
import Note from '../components/Note'
import LogoutButton from '../components/LogoutButton'
import '../styles/Home.css'


function Home() {
    const [notes, setNotes] = useState([]);
    const [content, setContent] = useState("")
    const [title, setTitle] = useState("")
    const [state, setState] = useState(true)
    const [currentUser, setCurrentUser] = useState(null)

    useEffect(() => {
        getNotes();
        getCurrentUser();
    }, []);

    const getNotes = async () => {
        api
            .get("/api/notes/")
            .then((res) => res.data)
            .then((data) => {setNotes(data); console.log(data) })
            .catch((err) => alert(err));
    };

    const getCurrentUser = async () => {
        api
            .get("/api/current_user/")
            .then((res) => res.data)
            .then((data) => { setCurrentUser(data.username); console.log("Current User:", data.username); })
            .catch((err) => alert(err));
    };

    const deleteNote = async (id) => {
        api
            .delete(`/api/notes/delete/${id}/`).then((res) => {
                if (res.status === 204) alert("Note deleted!")
                else alert("Failed to delete note")
                getNotes();
            })
            .catch((error) => alert(error));
        
    };

    const createNote = (e) => {
        e.preventDefault()
        api
            .post("/api/notes/", {content, title, state})
            .then((res) => {
                if (res.status === 201) alert("Note created!");
                else alert("Failed to make note")
                getNotes();
            })
            .catch((err) => alert(err));
        
    }

    return <div>
        <div>
            <h2>Notes</h2>
            {notes.map((note) => (
                (note.state || note.author_username === currentUser) ? <Note note={note} onDelete={deleteNote} key={note.id} /> : null
            ))}
        </div>
        <h2>Create a Note</h2>
        <form onSubmit={createNote}>
            <label htmlFor='title'>Title:</label>
            <br/>
            <input
                type='text'
                id='title'
                name='title'
                required
                onChange={(e) => setTitle(e.target.value)}
                value={title}
            />
            <label htmlFor='content'>Content:</label>
            <br/>
            <textarea 
            id="content" 
            name="content" 
            required 
            value={content} 
            onChange={(e) => setContent(e.target.value)}
            ></textarea>
            <br/>
            <label htmlFor='state'>State:</label>
                <select
                    id='state'
                    name='state'
                    required
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                >
                    <option value='true'>Public</option>
                    <option value='false'>Private</option>
                </select>
                <br/>
            <input type='submit' value='Submit'></input>
            <LogoutButton />
        </form>
    </div>
}

export default Home