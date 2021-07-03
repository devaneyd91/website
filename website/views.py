from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note, Pub_Note
from . import db
import json
from sqlite3 import Error
import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=None)

@views.route('members_area', methods=['GET', 'POST'])
@login_required
def members_area():
    if request.method == "POST":
        note = request.form.get('note')
        check1 = request.form.get('check1')
        
        if check1:
            
            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Pub_Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
        else:
            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
    
    
    return render_template("members_area.html", user=current_user)

@views.route('public_notes')
@login_required
def public_notes():
    notes = create_connection()

    return render_template("public_notes.html", user=current_user, pub_notes=notes)  
def create_connection():

    conn = sqlite3.connect(r'C:\Users\seang\Desktop\IN DEV\Devon\Website\website\database.db')
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM pub__note")
    rows = cur.fetchall()

    note_array = []
    for row in rows:
        note_array.append(Pub_Note(id=row[0], data=row[1], user_id=row[2], date=row[3]))

    
    return note_array
   

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
     
    return jsonify({})


    