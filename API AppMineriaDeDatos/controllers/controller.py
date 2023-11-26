from flask import jsonify, request
from models.models import *

mod_admin= Models()

class controller():

    def  login(self):
        query=mod_admin.login()
        return query
    
    def  predecir(self):
        query=mod_admin.predecir()
        return query

           
        
        
        
    
    