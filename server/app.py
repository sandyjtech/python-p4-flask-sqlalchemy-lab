from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Zoo app</h1>'

def format_attributes(attributes):
    return ''.join(f'<ul>{attr}</ul>' for attr in attributes)

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    attributes = [
        f'ID: {animal.id}',
        f'Name: {animal.name}',
        f'Species: {animal.species}',
        f'Zookeeper: {animal.zookeeper.name}',
        f'Enclosure: {animal.enclosure.environment}'
    ]
    response_body = format_attributes(attributes)
    return make_response(response_body)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    attributes = [
        f'ID: {zookeeper.id}',
        f'Name: {zookeeper.name}',
        f'Birthday: {zookeeper.birthday}',
        'Animals:',
        format_attributes(f'Animal: {animal.name}' for animal in zookeeper.animals)
    ]
    response_body = format_attributes(attributes)
    return make_response(response_body)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    attributes = [
        f'ID: {enclosure.id}',
        f'Environment: {enclosure.environment}',
        f'Open to Visitors: {enclosure.open_to_visitors}',
        'Animals:',
        format_attributes(f'Animal: {animal.name}' for animal in enclosure.animals)
    ]
    response_body = format_attributes(attributes)
    return make_response(response_body)

if __name__ == '__main__':
    app.run(port=5555, debug=True)