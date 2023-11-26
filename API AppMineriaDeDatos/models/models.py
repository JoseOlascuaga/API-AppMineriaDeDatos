from config import *
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder





class Models():
    
   def login(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        # Verificar el nombre de usuario y la contraseña en la base de datos
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        
        
        if not user:
            response = {
                'success': False,
                'message': 'Usuario o contraseña incorrectos'
            }
            return jsonify(response), 401
        

        # Generar el token JWT
        token_payload = {
            'sub': user[0],
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(token_payload, 'secret', algorithm='HS256')

        response = {
            'success': True,
            'message': 'Login exitoso',
            'token': token
        }
        return jsonify(response), 200
    
    
   def predecir(self):
    try:
        uploaded_file = request.files['file']
        df = pd.read_csv(uploaded_file)
        
        df['first_open'] = pd.to_datetime(df['first_open'])
        df['enrolled_date'] = pd.to_datetime(df['enrolled_date'])

        df['hour'] = pd.to_numeric(df['hour'].str.extract('(\d+)')[0], errors='coerce')

        le = LabelEncoder()
        df['screen_list_encoded'] = le.fit_transform(df['screen_list'])

        df['hour'].fillna(df['hour'].mean(), inplace=True)
        df['screen_list_encoded'].fillna(df['screen_list_encoded'].mode()[0], inplace=True)

        df['time_to_enroll'] = (df['enrolled_date'] - df['first_open']).dt.total_seconds()

        df = df.drop(['user', 'first_open', 'enrolled_date', 'screen_list'], axis=1)
        
        X = df.drop('enrolled', axis=1)
        y = df['enrolled']

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        model = SVC()
        model.fit(X, y)

        y_pred = model.predict(X)

        result = {'predictions': y_pred.tolist()}
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})
                

