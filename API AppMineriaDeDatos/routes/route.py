from flask import Flask, jsonify, request, Blueprint
from flask_cors import  cross_origin
from controllers.controller import *


conexion= controller()



usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/login', methods=['POST'])
@cross_origin()  
def login():
   return conexion.login()

@usuarios.route('/predecir', methods=['POST'])
@cross_origin()
def predecir():
   return conexion.predecir()





