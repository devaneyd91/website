from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note, Pubcoms, Pubnote
from . import db
import json
from sqlite3 import Error
import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("home.html", user=current_user)  
    else:
        return render_template("home.html", user=None)


@views.route('members_area', methods=['GET', 'POST'])
@login_required
def members_area():
    if request.method == "POST":
        note = request.form.get('note')
        name = request.form.get('first_name')
        check1 = request.form.get('check1')
        
        if check1:
            
            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Pubnote(first_name=current_user.first_name, data=note, user_id=current_user.id)
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

    return render_template("public_notes.html", user=current_user, Pubnotes=notes)  
def create_connection():

    conn = sqlite3.connect(r'website\database.db')
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM pubnote")
    rows = cur.fetchall()

    note_array = []
    for row in rows:
        note_array.append(Pubnote(id=row[0], first_name=row[1], data=row[2], user_id=row[3], date=row[4]))

    
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


@views.route('/delete-pubnote', methods=['POST'])
@login_required
def delete_pubnote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Pubnote.query.get(noteId)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        else:
            flash('Only the note creator or admin can delete notes!', category='error')
            
    
    return jsonify({})

    
@views.route('/comment-pubnote', methods=['POST'])
@login_required
def comment_pubnote():
    note = json.loads(request.data)
    noteId = note['noteId']
    comment = note['comment']
    
    
    new_comment = Pubcoms(first_name=current_user.first_name, public_note=noteId, data=comment, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    flash('Note added!', category='success')

            
    
    return jsonify({})
    


@views.route('/rate-pubnote', methods=['POST'])
@login_required
def post_rating():
    rating = json.loads(request.data)
    noteId = rating['noteId']
    rating = rating['rating']
    
    
    note = Pubnote.query.get(noteId)
    note.rating = rating
    db.session.commit()
    flash('Rating Added!', category='success')

            
    
    return jsonify({})