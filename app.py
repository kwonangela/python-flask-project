from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('avatar', user='postgres', password='', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Atla(BaseModel):
    name = CharField()
    nation = CharField()
    is_bender = BooleanField(default=True)

db.connect()
db.drop_tables([Atla])
db.create_tables([Atla])

Atla(name='Aang', nation='Air', is_bender=True).save()
Atla(name='Katara', nation='Water', is_bender=True).save()
Atla(name='Sokka', nation='Water', is_bender=False).save()
Atla(name='Toph', nation='Earth', is_bender=True).save()
Atla(name='Zuko', nation='Fire', is_bender=True).save()

app = Flask(__name__)

@app.route('/')
def index():
  return "ATLA character database. Do /character to see all characters and /character/<id> for a specific character."
@app.route('/character/', methods=['GET', 'POST'])    
@app.route('/character/<id>', methods=['GET', 'PUT', 'DELETE'])    

def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return model_to_dict(Atla.get(Atla.id == id))
        else:
            char_list = []
            for char in Atla.select():
                char_list.append(model_to_dict(char))
            return char_list

    if request.method == 'PUT':
        body = request.get_json()
        Atla.update(body).where(Atla.id == id).execute()
        return (f"Character {str(id)} has been updated.")

    if request.method == 'POST':
        new_char = dict_to_model(Atla, request.get_json())
        new_char.save()
        return jsonify({"success": True})
    
    if request.method == 'DELETE':
        Atla.delete().where(Atla.id == id).execute()
        return (f"Character {str(id)} deleted.")

app.run(port=5000, debug=True)

