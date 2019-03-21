from flask import request
from flask_restful import Resource, Api
from flask import jsonify
import pandas as pd
from app.api import bp
from app import app
from app import db
import json
from json import dumps
import pdb
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from app.models import Meal, Ingredient, Recipe, Unit
from sqlalchemy import func
import datetime


@bp.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([meal.to_dict() for meal in meals])

@bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients])

@bp.route('/meallist', methods=['GET'])
def get_meallist():
    ingredientID = request.args['ingredient']
    
    recipes = db.session.query(Recipe).filter(Recipe.ingredient_id == ingredientID)

    return jsonify([recipe.to_dict() for recipe in recipes])

@bp.route('/ingredientsformeals', methods=['GET'])
def get_ingredientsformeals():

    # Find values passed in as parameters
    mealsString = request.args['meals']
    mealsList = json.loads(mealsString)

    # Sum the total quantity for each ingredient
    ingredients = db.session.query(Ingredient.name, Unit.name, func.sum(Recipe.quantity).label('quantity')
    ).join(Unit
    ).filter(Recipe.meal.has(Meal.name.in_(mealsList))
    ).group_by(Ingredient.name, Unit.name
    ).all()

    # pdb.set_trace()

    ingredientsDictionary = []

    for ingredient in ingredients:
        ingredientsDictionary.append(
            {
                'name': ingredient[0],
                'unit': ingredient[1],
                'quantity': ingredient[2]
            }
        )
        
    return jsonify(ingredientsDictionary)


@bp.route('/tasklist', methods=['GET', 'POST'])
def post_tasklist():
    ingredientString = request.args['ingredient']
    ingredients = json.loads(ingredientString)

    # reverses list so first ingredients appear at the top
    ingredients.sort(key=lambda x: x['TJAisle'], reverse = True)

    mealsString = request.args['meals']
    meals = json.loads(mealsString)

    mealListString = ''
    for meal in meals:
        mealListString = mealListString + '(' + str(meal['Number']) + ') ' + meal['Meal']['name'] + ' '

    SCOPES = 'https://www.googleapis.com/auth/tasks'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('tasks', 'v1', http=creds.authorize(Http()))
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # The grocery list name includes the date
    tasklist = {
        'title': 'Grocery List ' + date
        }

    # Create new task list
    result = service.tasklists().insert(body=tasklist).execute()

    tasklist_id = result['id']

    for ingredient in ingredients:
        task = {
            'title': ingredient['name'] + ' (' + str(ingredient['quantity']) + ' ' + ingredient['unit'] + ')'
        }

        # Add new task to the list that was previously created
        # only if quantity is greater than 0
        if ingredient['quantity'] > 0:
            service.tasks().insert(tasklist=tasklist_id, body=task).execute()

    # Add the meals to the top of the list so we know we remember what we planned to make
    mealTask = {
        'title': mealListString
        }

    service.tasks().insert(tasklist=tasklist_id, body=mealTask).execute()
    
    return 'OK'
