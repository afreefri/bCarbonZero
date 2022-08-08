# Import Flask Library
from pickle import NONE
from sre_parse import State
from unicodedata import decimal, name
from flask import Flask, render_template, request, session, url_for, redirect
from datetime import datetime, timedelta
# for this you need to pip install python-dateutil
from dateutil.relativedelta import relativedelta
import pymysql.cursors  # used to connect with the database
import hashlib  # to hash passwords

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='',
                       db='bcarbonzero',  # change to the name of ur database
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


####################################################################################################
# homepage stuffs section -- COMPLETED


# homepage -- completed
@app.route('/')
def index():
    if 'accountType' in session:
        return render_template('index.html', account=session['accountType'])
    else:
        return render_template('index.html', account='none')


# volunteer button on homepage -- completed
@app.route('/volunteer')
def volunteer():
    cursor = conn.cursor()

    query = 'SELECT * FROM opportunity'
    cursor.execute(query)
    data = cursor.fetchall()

    for each in data:
        query = 'SELECT name FROM organization WHERE EIN = %s'
        cursor.execute(query, each['EIN'])
        name = cursor.fetchone()
        each['name'] = name['name']

    if 'city' in session:
        remove = []
        for each in data:
            if(session['city'].lower() not in each['city'].lower()):
                remove.append(each)

        for each in remove:
            data.remove(each)

        session.pop('city')

    if 'zip' in session:
        remove = []
        for each in data:
            if(session['zip'] not in each['zip_code']):
                remove.append(each)

        for each in remove:
            data.remove(each)

        session.pop('zip')

    cursor.close()
    return render_template('volunteer.html', data=data)


@app.route('/oppSearch', methods=['GET', 'POST'])
def oppSearch():
    city = request.form['city']
    zip = request.form['zip_code']

    if city != '':
        session['city'] = city

    if zip != '':
        session['zip'] = zip

    return redirect(url_for("volunteer"))


# recruit button on homepage -- completed
@app.route('/recruit')
def recruit():
    if('accountType' in session):
        if(session['accountType'] == 'organization'):
            return render_template('recruit.html')
    return redirect(url_for('signup'))


@app.route('/recruitForm', methods=['GET', 'POST'])
def recruitForm():
    title = request.form['post_title']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    description = request.form['description']

    cursor = conn.cursor()
    query = 'SELECT * FROM organization WHERE email = %s'
    cursor.execute(query, (session['email']))
    data = cursor.fetchone()

    EIN = data['EIN']
    date_posted = datetime.today()
    time_posted = datetime.now()
    # we will have all rewards be set to 10 for now (in the future, maybe we can figure out a system for the tokens assigned)
    reward = 10

    ins = 'INSERT INTO opportunity VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)'
    cursor.execute(ins, (EIN, date_posted, time_posted, title,
                   description, reward, city, state, zip_code))
    conn.commit()
    cursor.close()
    return redirect(url_for('applicants'))


# advertise button on home page -- completed
@app.route('/advertise')
def advertise():
    if('accountType' in session):
        if(session['accountType'] == 'vendor'):
            return render_template('advertise.html')
    return redirect(url_for('signup'))


@app.route('/advertiseForm', methods=['GET', 'POST'])
def advertiseForm():
    title = request.form['post_title']
    description = request.form['description']
    website = request.form['website_link']
    discount = request.form['redirect_link']

    cursor = conn.cursor()
    query = 'SELECT * FROM vendor WHERE email = %s'
    cursor.execute(query, (session['email']))
    data = cursor.fetchone()

    EIN = data['EIN']
    date_posted = datetime.today()
    time_posted = datetime.now()
    # we will have all costs set to a cetain number for now (in the future, maybe we can figure out a system for the tokens)
    cost = 20

    ins = 'INSERT INTO advertisement VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (EIN, date_posted, time_posted, title,
                   description, website, discount, cost))
    conn.commit()
    cursor.close()
    return redirect(url_for('postHistory'))


# products button on home page -- completed
@app.route('/advertisements')
def advertisements():
    cursor = conn.cursor()

    query = 'SELECT * FROM advertisement'
    cursor.execute(query)
    data = cursor.fetchall()

    for each in data:
        query = 'SELECT name FROM vendor WHERE EIN = %s'
        cursor.execute(query, each['EIN'])
        name = cursor.fetchone()
        each['name'] = name['name']

    if 'keyword' in session:
        remove = []
        for each in data:
            if(session['keyword'].lower() not in each['title'].lower()):
                remove.append(each)

        for each in remove:
            data.remove(each)

        session.pop('keyword')

    cursor.close()
    return render_template('advertisements.html', data=data)


@app.route('/productSearch', methods=['GET', 'POST'])
def productSearch():
    keyword = request.form['keyword']
    session['keyword'] = keyword

    return redirect(url_for("advertisements"))


####################################################################################################
# signup, login, logout, and account home section
# signup button on home page -- completed
@app.route('/signup')
def signup():
    return render_template('signup.html')


# volunteer signup -- completed
@app.route('/usersignup')
def usersignup():
    return render_template('usersignup.html')


@app.route('/userSignupAuth', methods=['GET', 'POST'])
def userSignupAuth():
    # grabs information from the forms
    email = request.form['userEmail']
    password = request.form['userPassword']
    confirmPassword = request.form['confirmPassword']

    cursor = conn.cursor()
    query = 'SELECT * FROM volunteer WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchone()

    error = None
    if(data):
        error = 'This account already exists. Please login instead!'
        cursor.close()
        return render_template('usersignup.html', error=error)
    elif(password != confirmPassword):
        error = 'Passwords must match!'
        cursor.close()
        return render_template('usersignup.html', error=error, email=email)
    else:
        ins = 'INSERT INTO volunteer VALUES(%s, %s, %s)'
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute(ins, (email, password, 0))
        conn.commit()
        cursor.close()
        return redirect(url_for('login'))


# organization signup -- completed
@app.route('/organizationsignup')
def organizationsignup():
    return render_template('organizationsignup.html')


@app.route('/orgsignupcontinued')
def orgsignupcontinued():
    return render_template('orgsignupcontinued.html')


@app.route('/orgSignupAuth', methods=['GET', 'POST'])
def orgSignupAuth():
    # grabs information from the forms
    ein = request.form['EIN']
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']

    cursor = conn.cursor()
    query = 'SELECT * FROM organization WHERE EIN = %s OR email = %s'
    cursor.execute(query, (ein, email))
    data = cursor.fetchone()
    cursor.close()

    error = None
    if(data):
        error = 'This account already exists.'
        return render_template('organizationsignup.html', error=error)
    elif(password != confirmPassword):
        error = 'Passwords must match!'
        return render_template('organizationsignup.html', error=error, email=email, ein=ein)
    else:
        password = hashlib.md5(password.encode()).hexdigest()
        session['EIN'] = ein
        session['email'] = email
        session['password'] = password
        return redirect(url_for('orgsignupcontinued'))


@app.route('/orgSignupAuthContinued', methods=['GET', 'POST'])
def orgSignupAuthContinued():
    # grabs information from the forms
    name = request.form['name']
    building = request.form['building_num']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip_code']
    phone = request.form['phone_number']
    mission = request.form['mission_statement']
    description = request.form['description']
    website = request.form['website']

    cursor = conn.cursor()
    ins = 'INSERT INTO organization VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (session['EIN'], name, session['email'], session['password'],
                   building, street, city, zip, state, phone, mission, description, website))
    conn.commit()
    cursor.close()

    for key in list(session.keys()):
        session.pop(key)

    return redirect(url_for('login'))


# vendor signup -- completed
@app.route('/vendorsignup')
def vendorsignup():
    return render_template('vendorsignup.html')


@app.route('/vendorSignupAuth', methods=['GET', 'POST'])
def vendorSignupAuth():
    # grabs information from the forms
    ein = request.form['EIN']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['comfirmPassword']
    website = request.form['website']

    cursor = conn.cursor()
    query = 'SELECT * FROM vendor WHERE EIN = %s OR email = %s'
    cursor.execute(query, (ein, email))
    data = cursor.fetchone()

    error = None
    if(data):
        error = 'This account already exists.'
        cursor.close()
        return render_template('vendorsignup.html', error=error)
    elif(password != confirmPassword):
        error = 'Passwords must match!'
        cursor.close()
        return render_template('vendorsignup.html', error=error, ein=ein, email=email, name=name, website=website)
    else:
        ins = 'INSERT INTO vendor VALUES(%s, %s, %s, %s, %s)'
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute(ins, (ein, email, password, website, name))
        conn.commit()
        cursor.close()
        return redirect(url_for('login'))


# login -- completed
@app.route('/login')
def login():
    if 'error' in session:
        return render_template('login.html', error=session['error'])

    return render_template('login.html')


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    acc_type = request.form['account_type']
    email = request.form['email']
    password = request.form['password']
    password = hashlib.md5(password.encode()).hexdigest()

    cursor = conn.cursor()
    if(acc_type == "volunteer"):
        query = 'SELECT * FROM volunteer WHERE email = %s and password = %s'
    elif(acc_type == "organization"):
        query = 'SELECT * FROM organization WHERE email = %s and password = %s'
    else:  # vendor
        query = 'SELECT * FROM vendor WHERE email = %s and password = %s'

    cursor.execute(query, (email, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        # save login info to session
        session['email'] = email
        session['accountType'] = acc_type

        if 'apply' in session:
            # for applying on opportunity page, redirect to another function that will add the info and redirect them appropriately
            return redirect(url_for('applying'))
        elif 'purchase' in session:
            # for purchasing on product page, redirect to another function that will add the info and redirect them appropriately
            return redirect(url_for('purchasing'))
        else:
            return redirect(url_for('account'))
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


# account home pages -- completed
@app.route('/account')
def account():
    cursor = conn.cursor()
    if(session['accountType'] == "volunteer"):
        query = 'SELECT * FROM volunteer WHERE email = %s'
        cursor.execute(query, (session['email']))
        data = cursor.fetchone()
        tokens = data['tokens_collected']
        cursor.close()
        return render_template('userhome.html', email=session['email'], tokens=tokens)
    elif(session['accountType'] == "organization"):
        query = 'SELECT * FROM organization WHERE email = %s'
        cursor.execute(query, (session['email']))
        data = cursor.fetchone()
        name = data['name']
        building_num = data['building_num']
        street = data['street']
        city = data['city']
        state = data['state']
        zip_code = data['zip_code']
        phone_num = data['phone_num']
        website = data['website']
        mission_statement = data['mission_statement']
        description = data['description']
        cursor.close()
        return render_template('organizationHome.html', name=name, building_num=building_num, street=street, city=city, state=state, zip_code=zip_code, phone_num=phone_num, website=website, email=session['email'], mission_statement=mission_statement, description=description)
    else:
        query = 'SELECT * FROM vendor WHERE email = %s'
        cursor.execute(query, (session['email']))
        data = cursor.fetchone()
        name = data['name']
        website = data['website']
        cursor.close()
        return render_template("vendorhome.html", name=name, website=website, email=session['email'])


# Logging out -- completed
@ app.route('/logout')
def logout():
    # clear everything in the session when you log out
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


####################################################################################################
# volunteer account page links -- COMPLETED


# view purchasing history -- completed
@app.route('/exchangeHistory')
def exchangeHistory():
    cursor = conn.cursor()

    query = 'SELECT * FROM exchange NATURAL LEFT OUTER JOIN advertisement WHERE email = %s'
    cursor.execute(query, (session['email']))
    data = cursor.fetchall()

    cursor.close()

    if 'error' in session:
        error = session['error']
        session.pop('error')
    else:
        error = None

    return render_template('exchangehistory.html', data=data, error=error)


# view volunteering history -- completed
@app.route('/volunteerHistory')
def volunteerHistory():
    cursor = conn.cursor()

    query = 'SELECT * FROM apply NATURAL LEFT OUTER JOIN opportunity WHERE email = %s'
    cursor.execute(query, (session['email']))
    data = cursor.fetchall()

    cursor.close()
    return render_template('volunteerHistory.html', data=data)


# edit user account information -- completed
@app.route('/userEditAccount')
def userEditAccount():
    return render_template('useraccountedit.html')


@app.route('/editUserPassword', methods=['GET', 'POST'])
def editUserPassword():
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password == confirm:
        password = hashlib.md5(password.encode()).hexdigest()
        cursor = conn.cursor()
        query = 'UPDATE volunteer SET password = %s WHERE email = %s'
        cursor.execute(query, (password, session['email']))
        conn.commit()
        cursor.close()
        return redirect(url_for('account'))
    else:
        error = "passwords must match!"
        return render_template('useraccountedit.html', passwordError=error)


# applying for opportunities on the opportunitypage -- completed
@app.route('/applyOpportunity/<ein>/<post_date>/<post_time>', methods=['GET', 'POST'])
def applyOpportunity(ein, post_date, post_time):
    if request.form.get('applybutton') == 'APPLY':
        if 'accountType' in session:  # if logged in
            if session['accountType'] == "volunteer":  # and is a volunteer
                session['post_ein'] = ein
                session['post_date'] = post_date
                session['post_time'] = post_time
                return redirect(url_for('applying'))
            else:
                session['error'] = "please log in / sign up as a volunteer"
                session['apply'] = True
                session['post_ein'] = ein
                session['post_date'] = post_date
                session['post_time'] = post_time
                return redirect(url_for('login'))  # must log in as a volunteer
        else:  # not logged in
            session['error'] = "please log in / sign up as a volunteer"
            session['apply'] = True
            session['post_ein'] = ein
            session['post_date'] = post_date
            session['post_time'] = post_time
            return redirect(url_for('login'))  # must log in as a volunteer


@app.route('/applying')
def applying():
    if session['accountType'] == "volunteer":
        cursor = conn.cursor()

        # check if already applied to
        query = 'SELECT * FROM apply WHERE email = %s AND EIN = %s AND date_posted = %s AND time_posted = %s'
        cursor.execute(query, (session['email'], session['post_ein'],
                       session['post_date'], session['post_time']))
        data = cursor.fetchone()

        if not data:
            query = 'INSERT INTO apply VALUES (%s,%s,%s,%s,0)'
            cursor.execute(query, (session['email'], session['post_ein'],
                                   session['post_date'], session['post_time']))
            conn.commit()

        cursor.close()

        if 'error' in session:
            session.pop('error')
        if 'apply' in session:
            session.pop('apply')
        session.pop('post_ein')
        session.pop('post_date')
        session.pop('post_time')

        return redirect(url_for('volunteerHistory'))

    else:
        return redirect(url_for('login'))


# purchase the discount on productpage -- completed
@app.route('/purchase/<ein>/<post_date>/<post_time>', methods=['GET', 'POST'])
def purchase(ein, post_date, post_time):
    if request.form.get('applybutton') == 'EXCHANGE 20 TOKENS':
        if 'accountType' in session:  # if logged in
            if session['accountType'] == "volunteer":  # and is a volunteer
                session['post_ein'] = ein
                session['post_date'] = post_date
                session['post_time'] = post_time
                return redirect(url_for('purchasing'))
            else:
                session['error'] = "please log in / sign up as a volunteer"
                session['purchase'] = True
                session['post_ein'] = ein
                session['post_date'] = post_date
                session['post_time'] = post_time
                return redirect(url_for('login'))  # must log in as a volunteer
        else:  # not logged in
            session['error'] = "please log in / sign up as a volunteer"
            session['purchase'] = True
            session['post_ein'] = ein
            session['post_date'] = post_date
            session['post_time'] = post_time
            return redirect(url_for('login'))  # must log in as a volunteer


@app.route('/purchasing')
def purchasing():
    if session['accountType'] == "volunteer":
        cursor = conn.cursor()

        # check if already applied to
        query = 'SELECT * FROM exchange WHERE email = %s AND EIN = %s AND date_posted = %s AND time_posted = %s'
        cursor.execute(query, (session['email'], session['post_ein'],
                       session['post_date'], session['post_time']))
        data = cursor.fetchone()

        if not data:
            # check if they have enough tokens
            query = 'SELECT * FROM volunteer WHERE email = %s'
            cursor.execute(query, session['email'])
            user = cursor.fetchone()
            tokens = user['tokens_collected']

            if tokens >= 20:  # they have enough
                tokens -= 20  # we are setting each purchase to be 20 tokens
                query = 'UPDATE volunteer SET tokens_collected = %s WHERE email = %s '
                cursor.execute(query, (tokens, session['email']))
                conn.commit()

                query = 'INSERT INTO exchange VALUES (%s,%s,%s,%s)'
                cursor.execute(
                    query, (session['email'], session['post_ein'], session['post_date'], session['post_time']))
                conn.commit()

            else:  # not enough tokens
                session['error'] = "You do not have enough tokens :("
                cursor.close()
                if 'purchase' in session:
                    session.pop('purchase')
                session.pop('post_ein')
                session.pop('post_date')
                session.pop('post_time')
                return redirect(url_for('exchangeHistory'))

        cursor.close()

        if 'error' in session:
            session.pop('error')
        if 'purchase' in session:
            session.pop('purchase')
        session.pop('post_ein')
        session.pop('post_date')
        session.pop('post_time')

        return redirect(url_for('exchangeHistory'))

    else:
        return redirect(url_for('login'))


####################################################################################################
# organization account page links -- COMPLETED


# edit organization account information -- completed
@app.route('/orgEditAccount')
def orgEditAccount():
    return render_template('orgeditaccount.html')


@app.route('/editOrgName', methods=['GET', 'POST'])
def editOrgName():
    name = request.form['name']

    cursor = conn.cursor()
    query = 'UPDATE organization SET name = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
    cursor.execute(query, (name, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


@app.route('/editOrgPassword', methods=['GET', 'POST'])
def editOrgPassword():
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password == confirm:
        password = hashlib.md5(password.encode()).hexdigest()
        cursor = conn.cursor()
        query = 'UPDATE organization SET password = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
        cursor.execute(query, (password, session['email']))
        conn.commit()
        cursor.close()
        return redirect(url_for('account'))
    else:
        error = "passwords must match!"
        return render_template('orgEditAccount.html', passwordError=error)


@app.route('/editOrgAddress', methods=['GET', 'POST'])
def editOrgAddress():
    building = request.form['building_num']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip_code']

    cursor = conn.cursor()
    query = 'UPDATE organization SET building_num = %s, street = %s, city = %s, state = %s, zip_code = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
    cursor.execute(query, (building, street, city,
                   state, zip, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


@app.route('/editOrgNumber', methods=['GET', 'POST'])
def editOrgNumber():
    number = request.form['phone_number']

    cursor = conn.cursor()
    query = 'UPDATE organization SET phone_num = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
    cursor.execute(query, (number, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


@app.route('/editOrgStatement', methods=['GET', 'POST'])
def editOrgStatement():
    statement = request.form['mission_statement']

    cursor = conn.cursor()
    query = 'UPDATE organization SET mission_statement = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
    cursor.execute(query, (statement, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


@app.route('/editOrgDescription', methods=['GET', 'POST'])
def editOrgDescription():
    description = request.form['description']

    cursor = conn.cursor()
    query = 'UPDATE organization SET description = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
    cursor.execute(query, (description, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


@app.route('/editOrgWebsite', methods=['GET', 'POST'])
def editOrgWebsite():
    website = request.form['website']

    cursor = conn.cursor()
    query = 'UPDATE organization SET website = %s WHERE EIN = (SELECT EIN FROM organization where email = %s)'
    cursor.execute(query, (website, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


# organization display post history and applicants -- completed
@app.route('/applicants')
def applicants():
    cursor = conn.cursor()

    # first find the EIN of our organization
    query = 'SELECT * FROM organization WHERE email = %s'
    cursor.execute(query, (session['email']))
    data = cursor.fetchone()
    ein = data['EIN']

    # then find all the posts that the organization posted (given their EIN)
    query = 'SELECT * FROM opportunity WHERE EIN = %s'
    cursor.execute(query, (ein))
    data = cursor.fetchall()

    # find all the applicants for each post
    query = 'SELECT * FROM apply WHERE EIN = %s'
    cursor.execute(query, (ein))
    applicants = cursor.fetchall()

    for opps in data:
        opps['applicants'] = []

    for opps in data:
        for user in applicants:
            if (opps['date_posted'] == user['date_posted']) and (opps['time_posted'] == user['time_posted']) and (opps['EIN'] == ein):
                opps['applicants'].append(user)

    cursor.close()

    return render_template('applicants.html', data=data)


# organization click opportunity page from applicants page -- completed
@app.route('/opportunityPage/<ein>/<post_date>/<post_time>')
def opportunityPage(ein, post_date, post_time):
    cursor = conn.cursor()

    query = 'SELECT * FROM opportunity WHERE EIN = %s AND date_posted = %s AND time_posted = %s'
    cursor.execute(query, (ein, post_date, post_time))
    data = cursor.fetchone()

    query = 'SELECT * FROM organization WHERE EIN = %s'
    cursor.execute(query, (ein))
    org = cursor.fetchone()

    cursor.close()

    return render_template('opportunitypage.html', data=data, name=org['name'])


# organization delete post -- completed
@app.route('/deletePost/<post_date>/<post_time>', methods=['GET', 'POST'])
def deletePost(post_date, post_time):
    cursor = conn.cursor()

    query = 'DELETE FROM opportunity WHERE EIN = (SELECT EIN FROM organization WHERE email = %s) AND date_posted = %s AND time_posted = %s '
    cursor.execute(query, (session['email'], post_date, post_time))
    conn.commit()

    cursor.close()
    return redirect(url_for('applicants'))


# organization approve applicants -- completed
@app.route('/approveApplicants/<post_date>/<post_time>', methods=['GET', 'POST'])
def approveApplicants(post_date, post_time):
    checked = request.form.getlist('applicantStatus')
    cursor = conn.cursor()

    for each in checked:
        query = 'UPDATE apply SET status = 1 WHERE EIN = (SELECT EIN FROM organization WHERE email = %s) AND date_posted = %s AND time_posted = %s AND email = %s '
        cursor.execute(query, (session['email'], post_date, post_time, each))
        conn.commit()

        # add the tokens to their account
        query = 'SELECT * FROM volunteer WHERE email = %s'
        cursor.execute(query, each)
        user = cursor.fetchone()
        tokens = user['tokens_collected']
        tokens += 10  # we set each volunteering opp w reward 10
        query = 'UPDATE volunteer SET tokens_collected = %s WHERE email = %s '
        cursor.execute(query, (tokens, each))
        conn.commit()

    # decline all the others who were not in the checked list
    query = 'SELECT * FROM apply WHERE EIN = (SELECT EIN FROM organization WHERE email = %s) AND date_posted = %s AND time_posted = %s'
    cursor.execute(query, (session['email'], post_date, post_time))
    applicants = cursor.fetchall()

    for each in applicants:
        if each['email'] not in checked:
            query = 'UPDATE apply SET status = 2 WHERE EIN = (SELECT EIN FROM organization WHERE email = %s) AND date_posted = %s AND time_posted = %s AND email = %s '
            cursor.execute(
                query, (session['email'], post_date, post_time, each['email']))
            conn.commit()

    # applicant approval/rejection has been updated
    query = 'UPDATE opportunity SET updated = 1 WHERE EIN = (SELECT EIN FROM organization WHERE email = %s) AND date_posted = %s AND time_posted = %s'
    cursor.execute(query, (session['email'], post_date, post_time))
    conn.commit()

    cursor.close()
    return redirect(url_for('applicants'))


# organization about page -- completed
@app.route('/organizationAbout/<EIN>')
def organizationAbout(EIN):
    cursor = conn.cursor()

    query = 'SELECT * FROM organization WHERE EIN = %s'
    cursor.execute(query, (EIN))
    data = cursor.fetchone()
    cursor.close()

    return render_template('organizationAbout.html', data=data)


####################################################################################################
# vendor account page links -- unfinished


# edit vendor account information -- completed
@app.route('/vendorAccountEdit')
def vendorAccountEdit():
    return render_template('vendoraccountedit.html')


@app.route('/editVendorName', methods=['GET', 'POST'])
def editVendorName():
    name = request.form['name']

    cursor = conn.cursor()
    query = 'UPDATE vendor SET name = %s WHERE EIN = (SELECT EIN FROM vendor where email = %s)'
    cursor.execute(query, (name, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


@app.route('/editVendorPassword', methods=['GET', 'POST'])
def editVendorPassword():
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password == confirm:
        password = hashlib.md5(password.encode()).hexdigest()
        cursor = conn.cursor()
        query = 'UPDATE vendor SET password = %s WHERE EIN = (SELECT EIN FROM vendor where email = %s)'
        cursor.execute(query, (password, session['email']))
        conn.commit()
        cursor.close()
        return redirect(url_for('account'))
    else:
        error = "passwords must match!"
        return render_template('vendorAccountEdit.html', passwordError=error)


@app.route('/editVendorWebsite', methods=['GET', 'POST'])
def editVendorWebsite():
    website = request.form['website']

    cursor = conn.cursor()
    query = 'UPDATE vendor SET website = %s WHERE EIN = (SELECT EIN FROM vendor where email = %s)'
    cursor.execute(query, (website, session['email']))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))


# vendor post history -- completed
@app.route('/postHistory')
def postHistory():

    cursor = conn.cursor()

    # first find the EIN of our vendor
    query = 'SELECT * FROM vendor WHERE email = %s'
    cursor.execute(query, (session['email']))
    data = cursor.fetchone()
    ein = data['EIN']

    # then find all the posts that the vendor posted (given their EIN)
    query = 'SELECT * FROM advertisement WHERE EIN = %s'
    cursor.execute(query, (ein))
    data = cursor.fetchall()

    # find all the customers for each post
    query = 'SELECT * FROM exchange WHERE EIN = %s'
    cursor.execute(query, (ein))
    customers = cursor.fetchall()

    for ad in data:
        ad['customers'] = []
        ad['total_customers'] = 0

    for ad in data:
        for user in customers:
            if (ad['date_posted'] == user['date_posted']) and (ad['time_posted'] == user['time_posted']) and (ad['EIN'] == ein):
                ad['customers'].append(user)
                ad['total_customers'] += 1

    cursor.close()

    return render_template('postHistory.html', data=data)


# product page -- completed
@app.route('/productPage/<ein>/<post_date>/<post_time>')
def productPage(ein, post_date, post_time):
    cursor = conn.cursor()

    query = 'SELECT * FROM advertisement WHERE EIN = %s AND date_posted = %s AND time_posted = %s'
    cursor.execute(query, (ein, post_date, post_time))
    data = cursor.fetchone()

    query = 'SELECT * FROM vendor WHERE EIN = %s'
    cursor.execute(query, (ein))
    vendor = cursor.fetchone()

    cursor.close()

    return render_template('productpage.html', data=data, name=vendor['name'])


# vendor delete ad -- completed
@app.route('/deleteAd/<post_date>/<post_time>', methods=['GET', 'POST'])
def deleteAd(post_date, post_time):
    cursor = conn.cursor()

    query = 'DELETE FROM advertisement WHERE EIN = (SELECT EIN FROM vendor WHERE email = %s) AND date_posted = %s AND time_posted = %s '
    cursor.execute(query, (session['email'], post_date, post_time))
    conn.commit()

    cursor.close()
    return redirect(url_for('postHistory'))


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
