#!/usr/bin/python

# IETF Meeting Registration Product
# Written by Matt Larson
# Copyright 2007 Association Management Solutions

#Import Modules
import cgi
#import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
import ConfigParser


def startpage():
    print """Content-type: text/html; charset = utf-8\n\n

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">

<html>"""

    print """
        <head>
        <title>%s</title>
         <style type = "text/css">
            td.reg {text-align: left; border-width: thin; border-style: solid; margin: 0px; padding: 2px; border-spacing: 0px; border-color: #26445B; font-size: 10pt;}
            td.regright {text-align: right; border-width: thin; border-style: solid; margin: 0px; padding: 2px; border-spacing: 0px; border-color: #26445B; font-size: 10pt;}
            td.regblk {text-align: left; border-width: thin; border-style: solid; margin: 0px; padding: 2px; border-spacing: 0px; border-color: #26445B; font-size: 10pt; color: #000000; font-weight: bold;}
            th.reg {border-width: thin; border-style: solid; margin: 0px; padding: 2px; border-spacing: 0px; border-color: #26445B; }
            table.reg { border-collapse: collapse; margin: 0px; padding: 0px; border-spacing: 0px; }
            input.reg { font-family: Arial; color: #000000; font-weight: bold; font-size: 10pt; }
            select.reg { font-family: Arial; color: #36546B; font-weight: bold; font-size: 10pt; }
            h2 { font-family: Arial; color: #26445B; }
            td { font-family: Arial; color: #26445B; }
            td.letter { font-family: Arial; color: #000000; font-size: 10pt }
            td.letterdata { font-family: Arial; color: #000000; font-weight: bold; font-size: 10pt }
            th { font-family: Arial; color: #26445B; font-weight: bold; }
            </style>

        </head>
    <body>""" % "NomCom Volunteer Validation Tool"

def querymulti(query, host, db, user, password):
    value = 0
    # connect
    db = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
    # create a cursor
    cursor = db.cursor()
    # execute SQL statement
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def querysingle(query, host, db, user, password):
    value = 0
    # connect
    db = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
    # create a cursor
    cursor = db.cursor()
    # execute SQL statement
    cursor.execute(query)
    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)
    # get and display one row at a time
    row = cursor.fetchone()
    try:
        value = row[0]
    except:
        value = 0
    cursor.close()
    return value

def getmeetingnumbers():
    meetinglist = [97, 98, 99, 100, 101]
    return meetinglist

def checkbyconfirmation(confirmno):
    confirmno = "%s" % confirmno
    db = confirmno[0:2]
    ## Ugly hack for IETF 100 onward
    if db == "10":
        db = 100
    if db == "11":
        db = 101
    if db == "12":
        db = 102
    if db == "13":
        db = 103
    if db == "14":
        db = 104

    dbname = "ietf%s" % db
    rsn = confirmno[0:6]
    pw = confirmno[6:11]

    query = """select rsn from registrations where rsn = %s and password = %s""" % (rsn, pw)
    result = querymulti(query, "localhost", dbname, dbuser, dbpass)
    if len(result) == 0:
        return "Invalid confirmation number"

    query = """select fname, lname, email, rsn, password from registrations where rsn = %s and password = %s and checkindate > "0000-00-00 00:00:00" and regtype < 2""" % (rsn, pw)
    result = querymulti(query, "localhost", dbname, dbuser, dbpass)
    output = []

    for row in result:
        output.append(db)
        output.append(row[0])
        output.append(row[1])
        output.append(row[2])
        fullrsn = "%s%s" % (row[3], row[4])
        output.append(fullrsn)

    return output

def checknumbers(confirmlist):
    output = []
    for number in confirmlist:
        result = checkbyconfirmation(number)
        if result == "Invalid confirmation number":
            continue
        if result != []:
            output.append(result)

    return output

def checkbyemail(meetinglist, emails):
    masterresult = []
    for email in emails:
        query = """select fname, lname, email, rsn, password from registrations where email = "%s" and checkindate > "0000-00-00 00:00:00" and regtype < 2""" % email

        for meeting in meetinglist:
            output = []
            dbname = "ietf%s" % meeting
            result = querymulti(query, "localhost", dbname, dbuser, dbpass)
            for row in result:
                output.append("%s" % meeting)
                output.append(row[0])
                output.append(row[1])
                output.append(row[2])
                fullrsn = "%s%s" % (row[3], row[4])
                output.append(fullrsn)
            if output != []:
                masterresult.append(output)

    return masterresult

def checkbyname(meetinglist, names):
    masterresult = []
    for name in names:
        query = """select fname, lname, email, rsn, password from registrations where fname = "%s" and lname = "%s" and checkindate > "0000-00-00 00:00:00" and regtype < 2""" % (name[0], name[1])

        for meeting in meetinglist:
            output = []
            dbname = "ietf%s" % meeting
            result = querymulti(query, "localhost", dbname, dbuser, dbpass)
            for row in result:
                output.append("%s" % meeting)
                output.append(row[0])
                output.append(row[1])
                output.append(row[2])
                fullrsn = "%s%s" % (row[3], row[4])
                output.append(fullrsn)
            if output != []:
                masterresult.append(output)

    return masterresult

def addlists(target, source):
    tlen = len(target)
    slen = len(source)

    for i in range(0, slen):
        match = 0
        for j in range(0, tlen):
            if source[i][0] == target[j][0]:
                match = 1
        if match == 0:
            newline = [source[i][0], source[i][1], source[i][2], source[i][3]]
            target.append(newline)

def displayform(form, meetinglist):

    print"""<TABLE class = "reg" width = 800><TR><TH class = "reg" colspan = 2><font size = 4>NomCom Volunteer Validation Tool</TH></TR>"""
    print"""<TR><TD colspan = 2 class = "reg"><font size = 3>Thank you for your interest in the IETF NomCom.<BR><BR>In order to be eligible to volunteer for the NomCom, a
    person must have attended three (3) out of the last (5) meetings.  This tool will check your attendance against the last five meetings:<UL>"""
    for meeting in meetinglist:
        print"""<LI>IETF%i""" % meeting
    print"""</UL>If you have attended at least three of these meetings, you will be considered eligible to volunteer.
    If you are interested in volunteering, you can contact the NomCom Chair and let them know that you would like to be included in the pool of volunteers.<BR><BR>Please note that single day pass attendance at a meeting does not
    meet the requirements for NomCom eligibility.<BR><BR>For further information on NomCom eligibility, please see:

    <UL>
    <LI><a href = "https://www.ietf.org/rfc/rfc7437.txt">RFC 7437</a>
    <LI><a href = "http://www.ietf.org/iesg/statement/nomcom-eligibility-and-day-passes.html">IESG Statement on NomCom Eligibility and Day Passes.</a>
    </UL></font></TD></TR>"""
    print"""<TR><TD class = "reg" colspan = 2>
    <b>Form Instructions</b><BR><BR>
    It is recommended that users initially try searching the attendance database by email address.  If the email address results do not return as many attendance
    records as you anticipated, then please try the search by confirmation numbers or by name.<BR><BR>
    You may provide up to 5 email addresses, names, or confirmation numbers for your search.  You only need to provide a unique identifier once.  For example, if you
    always register with the same email address, you only need to enter it in one of the 5 available boxes.<BR><BR>
    Once the form is submitted, you will receive a report listing the meetings you attended.
    If your attendance at three or more meetings has not been verified, you can re-submit the search with additional information.<BR><BR></TD></TR>"""
    print"""<TR><form name = "search" action = "nomcom.py" method = "post"><TH class = "reg">E-Mail Addresses</TH><TD class = "reg">"""
    for i in range(0, 5):
        print"""<input type = "text" name = "email" size = 40><BR>"""
    print"""</TD></TR>"""
    print"""<TR><form name = "search" action = "nomcom.py" method = "post"><TH class = "reg">Name (First, Last)</TH><TD class = "reg">"""
    for i in range(0, 5):
        print"""<input type = "text" name = "fname" size = 20><input type = "text" name = "lname" size = 20><BR>"""
    print"""</TD></TR>"""
    print"""<TR><form name = "search" action = "nomcom.py" method = "post"><TH class = "reg">Confirmation Numbers</TH><TD class = "reg">"""
    for i in range(0, 5):
        print"""<input type = "text" name = "confirmno" size = 15><BR>"""
    print"""</TD></TR>"""
    print"""<input type = "hidden" name = "rid" value = 1>"""
    print"""<input type = "hidden" name = "confirmno" value = "">"""
    print"""<TR><TD class = "reg" colspan = 2><CENTER><input type = "Submit" value = "Submit"></TD></TR></TABLE>"""

def makenames(fnames, lnames):
    namelist = []
    addname = []
    for i in range(0, 5):
        try:
            fn = fnames[i]
        except:
            fn = ""
        try:
            ln = lnames[i]
        except:
            ln = ""
        addname = [fn, ln]
        namelist.append(addname)

    return namelist

def makeunique(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output

startpage()
meetinglist = getmeetingnumbers()
meetinglist.sort()

## Parse config file for database user and password.
## This script should run with a select-only db account
myconfig = ConfigParser.ConfigParser()
myconfig.read('nomcomtool.cfg')
dbuser = myconfig.get('nomcomtool', 'dbuser')
dbpass = myconfig.get('nomcomtool', 'dbpass')



form = cgi.FieldStorage()
rid = form.getvalue("rid", 0)

if rid == 0:
    displayform(form, meetinglist)

if rid == "1":
    emails = form.getlist("email")
    fnames = form.getlist("fname")
    lnames = form.getlist("lname")
    confnos = form.getlist("confirmno")
    names = makenames(fnames, lnames)

    emails = makeunique(emails)
    names = makeunique(names)
    confnos = makeunique(confnos)

    emaillist = checkbyemail(meetinglist, emails)
    namelist = checkbyname(meetinglist, names)
    conflist = checknumbers(confnos)

    masterlist = []
    addlists(masterlist, emaillist)
    addlists(masterlist, namelist)
    addlists(masterlist, conflist)

    print"""<TABLE class = "reg" width = 800><TR><TH colspan = 2 class = "reg"><font size = 4>NomCom Volunteer Validation Tool - Search Results</TH></TR>"""

    if masterlist != []:
        print"""<TR><TD class = "reg">The search returned the following attendance records:<BR><BR><TABLE cellpadding = 5><TR><TH>Meeting No</TH><TH>First Name</TH><TH>Last Name</TH><TH>Email</TH></TR>"""
        for line in masterlist:
            print"""<TR>"""
            for i in range(0, 4):
                print"""<TD>%s</TD>""" % line[i]
            print"""</TR>"""
        print"""</TABLE><BR>"""
    else:
        print"""<TR><TD class = "reg">Sorry, no results matched search criteria.<BR><BR>"""

    print"""Based on the attendance results, you """
    if len(masterlist) < 3:
        print"""<font color = "red"><b>are not</b></font> qualified to volunteer for the NomCom, having attended %i of the last 5 meetings.<BR><BR>You may use the "back" button on your browser to submit additional search criteria (alternate names, confirmation numbers, email addresses) and search again.  If you beleive you are qualified for the NomCom but are unable to get the tool to locate your attendance records, please email the IETF Registrar.""" % len(masterlist)
    else:
        print"""<font color = "green"><b>are</b></font> qualified to volunteer for the NomCom, having attended %i of the last 5 meetings.""" % len(masterlist)

    print"""</TD></TR>"""
