import React from "react"
import '../styles/Note.css'

function Note({note, onDelete}) {
    const formattedDate = new Date(note.created_at).toLocaleDateString("en-US")

    return (
        <div className="note-container">
            <p className="note-title">Title：{note.title}</p>
            <p className="note-content">Content：<br/><br/>{note.content}</p>
            <p className="note-date">Note-Date：{formattedDate}</p>
            <p className="note-author">Author：{note.author_username}</p>
            <button className="delete-button" onClick={() => onDelete(note.id)}>
                Delete
            </button>
        </div>
    );
}

export default Note