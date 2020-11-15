from flask import Flask, render_template, request, session, jsonify
from classDbQueries import classDbQueries
from flask_cors import CORS, cross_origin
from datetime import datetime
import json
import sys
import time

dbStuff = classDbQueries()
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

@application.route('/')
def home():
    dbStuff = classDbQueries()
    diProp = dbStuff.getTestRecord()
    return jsonify(diProp)

@application.route('/api/login/<user>/<passw>')
def all(user,passw):
    if(user == '31w' and passw == 'turtle212power'):
        return jsonify(1)
    return jsonify(0)

@application.route('/api/property/<filter1>/asc/<startRecord>', methods=["GET","POST"])
def filterProperties(filter1,startRecord):
    ## default search parameters
    searchField = "owner_name"
    operator = "like"
    searchString = ""
    sort = "asc"
    # startRecord = 0
    limit = 1000
    ## check for post parameters to filter by
    if request.method == "POST":
        postParameters = json.loads(request.data)
        searchString = postParameters['filter2_search_string']
        if postParameters['filter2_field'] == 'property_address_contains':
            searchField = "property_address"
            operator = "like"
        elif postParameters['filter2_field'] == "property_address_does_not_contain":
            searchField = "property_address"
            operator = "not like"
        elif(postParameters['filter2_field'] == "owner_name_contains"):
            searchField = "owner_name"
            operator = "like"
        elif(postParameters['filter2_field'] == "owner_name_does_not_contain"):
            searchField = "owner_name"
            operator = "not like"
        elif(postParameters['filter2_field'] == "owner_address_contains"):
            searchField = "owner_address"
            operator = "like"
        elif(postParameters['filter2_field'] == "owner_address_does_not_contain"):
            searchField = "owner_address"
            operator = "not like"
        elif(postParameters['filter2_field'] == "notes_contains"):
            searchField = "notes"
            operator = "like"
        elif(postParameters['filter2_field'] == "notes_does_not_contain"):
            searchField = "notes"
            operator = "not like"
    dbStuff = classDbQueries()
    # print("filter1: " + filter1)
    # print("search field: " + searchField)
    # print("operator: " + operator)
    # print("search string: " + searchString)
    # print("sort: " + sort)
    # print("start record: " + str(startRecord))
    # print("limit: " + str(limit))
    diPropRecords = dbStuff.getPropRecords(filter1,searchField,operator,searchString,sort,startRecord,limit)
    if diPropRecords == []: return jsonify("aaa76")
    liNotes = dbStuff.getNotesRecords()
    diPropRecords = mergeNotes(diPropRecords,liNotes)
    liMailings = dbStuff.getMailingRecords()
    diPropRecords = mergeMailings(diPropRecords,liMailings)
    return jsonify(diPropRecords)

@application.route('/api/add_note/<pid>', methods=["POST"])
def addNote(pid):
    postParameters = json.loads(request.data)
    dbStuff = classDbQueries()
    diPropRecords = dbStuff.addNote(pid,postParameters['note'])
    return jsonify("ddd82")

@application.route('/api/delete_note/<noteId>', methods=["POST"])
def deleteNote(noteId):
    postParameters = json.loads(request.data)
    dbStuff = classDbQueries()
    resultDeleteNote = dbStuff.deleteNote(noteId)
    return jsonify("ddd96")

@application.route('/api/add_mailing/<pid>', methods=["POST"])
def addMailing(pid):
    postParameters = json.loads(request.data)
    dbStuff = classDbQueries()
    resultAddMailing = dbStuff.addMailing(pid)
    return jsonify("ddd91")

def mergeNotes(diPropRecords,liNotes):
    i=0
    while i<len(diPropRecords):
        match = 0
        for j,note in enumerate(liNotes):
            if note['pid'] == diPropRecords[i]['pid'] and match == 0:
                diPropRecords[i]['notes'] = []
                diPropRecords[i]['notes'].append({
                    "noteId": note['id'],
                    "note": datetime.fromtimestamp(int(note['time'])).strftime("%d-%b-%y") + ": " + note['notes']
                    })
                match = 1
            elif note['pid'] == diPropRecords[i]['pid'] and match == 1:
                diPropRecords[i]['notes'].append({
                    "noteId": note['id'],
                    "note": datetime.fromtimestamp(int(note['time'])).strftime("%d-%b-%y") + ": " + note['notes']
                    })
        else:
            i+=1
    return diPropRecords

def mergeMailings(diPropRecords,liMailings):
    i=0
    while i<len(diPropRecords):
        match = 0
        for j,m in enumerate(liMailings):
            if m['pid'] == diPropRecords[i]['pid'] and match == 0:
                diPropRecords[i]['mailings'] = []
                diPropRecords[i]['mailings'].append(m['date_mailed'].strftime("%d-%b-%y"))
                match = 1
            elif m['pid'] == diPropRecords[i]['pid'] and match == 1:
                diPropRecords[i]['mailings'].append(m['date_mailed'].strftime("%d-%b-%y"))
        else:
            i+=1
    return diPropRecords

if __name__ == "__main__":
    application.run()
