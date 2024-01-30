#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Length
from wtforms import StringField, SelectField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#db.init_app(app) 

HeroPower = db.Table(

    'heroes_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('heroes.id')),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id')),
    db.Column('strength', db.String)
 )
class HeroPowerForm(FlaskForm):
    strength = SelectField('Strength', choices=[('Strong', 'Strong'), ('Weak', 'Weak'), ('Average', 'Average')])
#Heroes Table
class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    powers = db.relationship('Power',secondary =HeroPower,back_populates = 'heroes')

# Powers Table
class Power(db.Model):
    __tablename__ = 'powers'
    description = StringField('Description', validators=[InputRequired(),Length(min =20)])
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    heroes = db.relationship('Hero',secondary =HeroPower, back_populates = 'powers')


 
def create_app():
    with app.app_context():
        db.create_all()

create_app()
 
@app.route('/')
def home():
    return <h1>Home</h1>
# Getting all hero
@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    heroes = Hero.query.all()
    heroes_info = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_info)

# Getting a single hero
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_single_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_info = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}
        return jsonify(hero_info)
    else:
        return jsonify({"error": "Hero not found"}), 404

# Getting all powers
@app.route('/powers', methods=['GET'])
def get_all_powers():
    powers = Power.query.all()
    powers_info = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_info)

# Getting a single power
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_single_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_info = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_info)
    else:
        return jsonify({"error": "Power not found"}), 404

# Updating powers
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        data = request.json
        updated_name = data.get('name', power.name)
        updated_description = data.get('description', power.description)
        return jsonify({'name': updated_name, 'description': updated_description})
    else:
        return jsonify({"error": "Power not found"}), 404

# Adding new hero_powers
@app.route('/heroes_powers', methods=['POST'])
def add_hero_power():
    if db.heroes_powers:
        data = request.json
        new_hero_power = HeroPower(strength=data['strength'], power_id=data['power_id'], hero_id=data['hero_id'])
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify({'strength': new_hero_power.strength, 'power_id': new_hero_power.power_id, 'hero_id': new_hero_power.hero_id}) 
    else:
        return jsonify({"error": "validation errors"})
if __name__ == '_main_':
    app.run(port=5555)
