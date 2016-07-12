import models
import data
import server
import requests
import json




#CreateNewUser will be called in server.py when a user logging in has not been found in database
def createNewUser(name_response, genotype_response):
    #Grab the dnaPairs at relative snps
    genome_data = genotype_response.json()

    # object with snp: gene properties 
    #Define the user's basic information
    user_first_name = name_response.json()['profiles'][0]['first_name']
    user_id = name_response.json()['profiles'][0]['id']

    
    #Create a new user following the Users Model
    new_user = models.User(user_id, user_first_name, genome_data)


    # Add the user to the database and commit it
    models.db_session.add(new_user)
    models.db_session.commit()


#
def createSnpsTable():
    

    # if snp database is empty 
    if len(models.db_session.query(models.Snp).all()) == 0:

       

        for snp in data.snps:
            new_snp = models.Snp(snp['title'], snp['rsid'], snp['pair'], snp['outcome'], snp['r'], snp['healthtip'])
            models.db_session.add(new_snp)
            models.db_session.commit()


    print json.loads(response.text)
