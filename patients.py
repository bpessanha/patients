#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__, static_url_path = "")
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

patients = [
    {
        'id': 1,
        'gender': u'male',
        'age': u'25', 
        'height': u'180', 
        'weight': u'90'
    },
    {
        'id': 2,
        'gender': u'female',
        'age': u'32',
        'height': u'170',
        'weight': u'86'
    }
]

def make_public_patient(patient):
    new_patient = {}
    for field in patient:
        if field == 'id':
            new_patient['uri'] = url_for('get_patient', patient_id = patient['id'], _external = True)
        else:
            new_patient[field] = patient[field]
    return new_patient
    
@app.route('/cercacor/api/patients', methods = ['GET'])
def get_patients():
    return jsonify( { 'patients': map(make_public_patient, patients) } )

@app.route('/cercacor/api/patients/<int:patient_id>', methods = ['GET'])
def get_patient(patient_id):
    patient = filter(lambda t: t['id'] == patient_id, patients)
    if len(patient) == 0:
        abort(404)
    return jsonify( { 'patient': make_public_patient(patient[0]) } )

@app.route('/cercacor/api/patients', methods = ['POST'])
def create_patient():
    if not request.json or not 'gender' in request.json:
        abort(400)
    patient = {
        'id': patients[-1]['id'] + 1,
        'gender': request.json['gender'],
        'age': request.json('age'),
        'height': request.json['height'],
        'weight': request.json['weight']
    }
    patients.append(patient)
    return jsonify( { 'patient': make_public_patient(patient) } ), 201

@app.route('/cercacor/api/patients/<int:patient_id>', methods = ['PUT'])
def update_patient(patient_id):
    patient = filter(lambda t: t['id'] == patient_id, patients)
    if len(patient) == 0:
        abort(404)
    if not request.json:
        abort(400)
    patient[0]['gender'] = request.json.get('gender', patient[0]['gender'])
    patient[0]['age'] = request.json.get('age', patient[0]['age'])
    patient[0]['height'] = request.json.get('height', patient[0]['height'])
    patient[0]['weight'] = request.json.get('weight', patient[0]['weight'])
    return jsonify( { 'patient': make_public_patient(patient[0]) } )
    
@app.route('/cercacor/api/patients/<int:patient_id>', methods = ['DELETE'])
def delete_patient(patient_id):
    patient = filter(lambda t: t['id'] == patient_id, patients)
    if len(patient) == 0:
        abort(404)
    patients.remove(patient[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)
