# this is python/flask server
# flask is a python based framwork, similar to django or express
# importing necessary modules 
import requests
import flask
from flask import Flask, request, render_template, jsonify, redirect, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
import jwt
from logging import Formatter, FileHandler
import controller
from os import path
import models
import os
from threading import Thread
import snps 
import random

# Should Gather data from config.py
   
BASE_CLIENT_URL = 'http://localhost:%s/'% PORT
CLIENT_ID = app.config.get('CLIENT_ID')
CLIENT_SECRET = app.config.get('CLIENT_SECRET')
REDIRECT_URI = app.config.get('REDIRECT_URI')
SECRET_KEY = app.config.get('SECRET_KEY')

#Initialize Flask application, for both production and local environments 
app = Flask(__name__)
PORT = int(os.environ.get('PORT', 1574))
is_prod = os.environ.get('IS_HEROKU', None)
app.config.from_object('config')


#all variables needed for 23AndMe API Call

SNPS=['rs761100', 'rs12340895', 'rs10488631', 'rs2287622', 'rs3803662', 'rs1219648', 'rs6025', 'rs6457617', 'rs3923809', 'rs1061147', 'rs1805007', 'rs2165241', 'rs2395185', 'rs9273363', 'rs2187668', 'rs2066844', 'rs2200733', 'rs1064395', 'rs10995190', 'rs7524102', 'rs2235529', 'rs7754840', 'rs7850258']
SCOPE = 'names basic email ancestry relatives genomes %s' % (' '.join(SNPS))
API_URL = 'https://api.23andme.com/'
SNP = (' '.join(SNPS))

# encoder 

def encode(pid, name, key):
    secrettoken = jwt.encode({'user_profile_id': pid,'user_first_name': name }, key, algorithm='HS256')
    return secrettoken


# defining our routes 


# exchange the auth code for a token, by sendimg a POST/token/ request with parameters of 
# client_Id and client_secret 
# this endpoint is the redirect uri 
@app.route('/receive_code/')

def receive_code():
    parameters = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }

    # in a requests.post HTTP request, you give parameters of url, data in the form of an object to be passed into the url's query string, and verify
    # you are requesting a token via a POST request to the 
    response = requests.post(
        "%s%s" % (API_URL, "token/"),
        data = parameters,
        verify=False
    )

    #get access token from 23andMe
    if response.status_code == 200:
        access_token = response.json()['access_token']
        headers = {'Authorization': 'Bearer %s' % access_token}


        # GETTING THE DATA

        #Begin API calls to 23andMe to get all scoped user data
        # maybe add more scoped data
        # print this to see what the responses are 
        name_response = requests.get('%s%s' % (API_URL, '1/demo/names/'), 
                                        headers = headers,
                                        verify=False)




        user_profile_id = name_response.json()['profiles'][0]['id']

       
       


        genotype_response = requests.get("%s%s" % (API_URL, "1/demo/genotypes/SP1_MOTHER_V4"),
                                        params={'locations': ' '.join(SNPS)},
                                        headers=headers,
                                        verify=False)
       
        
       

        user_response = requests.get("%s%s" % (API_URL, "1/demo/user/?email=true"),
                                        headers=headers,
                                        verify=False)

    
        
        #if both API calls are successful, process user data
        # PROCESSING THE DATA

        if user_response.status_code == 200 and genotype_response.status_code == 200 and name_response.status_code == 200:

           
            #user_first_name = name_response.json()['first_name']

            user_first_name = name_response.json()['profiles'][0]['first_name']

            #create additional thread to retrieve entire genome
            code = request.args.get('code')
            #genomeThread = Thread(target=controller.getGenome, args=(code,user_profile_id, headers))
            #genomeThread.start()


            if len(models.db_session.query(models.User).filter_by(profile_id=user_profile_id).all()) != 0:

                response = make_response(redirect(url_for('getUser')))
                response.set_cookie('user_first_name', user_first_name)
                response.set_cookie('token', encode(user_profile_id, user_first_name, SECRET_KEY))
                return response

         
            else:       
            # create user table                      
                controller.createNewUser(name_response, genotype_response)
           
            #create snps table
                controller.createSnpsTable()

            #render index.html and set cookie 
                response = make_response(render_template('index.html'))
                response.set_cookie('user_first_name', user_first_name)
                response.set_cookie('token', encode(user_profile_id, user_first_name, SECRET_KEY))
                return response
        #error handling if api calls for additional user data to 23andMe fail
        else:
            reponse_text = genotype_response.text
            response.raise_for_status()
    #error handling if initial api calls to 23andMe fail

@app.route('/')
# for our homepage endpoint, anytime we refresh the page
def home():
    # To authentication with 23andme API, we send users to https://api.23andme.com/authorize/, with below parameters of 
    # redirect_uri, response_type, client_ID, scope, and (state)  
    # you are asking users permission for their data, and if they accept you get an authorization code 
    # this is the BRANDED BUTTON as specified on 23andME site
    auth_url = 'https://api.23andme.com/authorize/?response_type=code&redirect_uri=%s&client_id=%s&scope=%s' % (REDIRECT_URI, CLIENT_ID, SCOPE)
    # render_template in python - allows you to render a specified template (in this case, landing.html), and variables yo uwn tto pass in 
    # flask will look for templates in the template folder 
    return render_template('landing.html', auth_url=auth_url)



@app.route('/get_info/')
def getUser():
    return render_template('index.html')
   



@app.route('/user/snpinfo/', methods=['POST', 'GET'])  #we should take out 'GET'?
def getSnps():

    token = request.cookies.get('token')
    jwtdecode = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    current_user_profile_id = jwtdecode['user_profile_id']

    user_snps = {}
    user_outcomes = []

    user = models.db_session.query(models.User).filter(models.User.profile_id == current_user_profile_id).first()
    user_data = user.serialize()
    for data in user_data:
        if data[:2:].lower()=='rs':
            user_snps[data] = user_data[data]

    
    for user_snp in user_snps:
        # loop through entire snp table, if any of snp base pairs match up to the base pair in user snps, put in an object with rsid and outcome
        current_snp = models.db_session.query(models.Snp).filter(models.Snp.rsid == user_snp).filter(models.Snp.pair == user_snps[user_snp]).first()



        if current_snp is not None:
            user_outcomes.append({"title": current_snp.serialize()["title"], "rsid": user_snp, "pair": user_snps[user_snp], "outcome": current_snp.serialize()['outcome'], "r": current_snp.serialize()['r'], 'healthtip': current_snp.serialize()['healthtip']});

    outcomes = {'outcomes': user_outcomes}
    return jsonify(outcomes)
   






#Initialize python server on port
if __name__ == '__main__':
  print 'Server has been initialized'
  if is_prod:
      app.run(host='0.0.0.0', port=PORT)
  else:
      app.run(debug=True, port=PORT)
