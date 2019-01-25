from __future__ import print_function
from flask import Flask, request
from flask_restful import Resource, Api
import json
from json import dumps
import pandas as pd
import pdb

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

app = Flask(__name__)

from app import routes

api = Api(app)

dataFilePathString = r"C:\Users\matte\grocery-list\app\example.xlsx"

class Meals(Resource):
	def get(self):

		# "r" is required at the start of the string so that it knows that it doesnt have an issue with character escapes. r = raw
		xl = pd.ExcelFile(dataFilePathString) 
		df1 = xl.parse('Meals')

		# Records is the preferred return format for this: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
		return df1.to_json(orient='records')

class AllIngredients(Resource):
	def get(self):

		xl = pd.ExcelFile(dataFilePathString) 
		df1 = xl.parse('Recipes')

		distinctIngredients = df1['Ingredient'].unique().tolist()

		return json.dumps(distinctIngredients)

class MealList(Resource):
	def get(self):
		ingredient = request.args['ingredient']
		
		xl = pd.ExcelFile(dataFilePathString) 
		df1 = xl.parse('Recipes')

		df = df1[df1.Ingredient == ingredient]

		return df.to_json(orient='records')

class Ingredients(Resource):
	def get(self):
		
		# Find values passed in as parameters
		mealsString = request.args['meals']
		mealsList = json.loads(mealsString)
		# pdb.set_trace() - used for debugging

		xl = pd.ExcelFile(dataFilePathString)
		df1 = xl.parse('Recipes')

		# only want ingredients for the meals that were passed in as an argument
		df = df1[df1.Meal.isin(mealsList)]
		s = df.groupby(['Ingredient', 'Unit', 'TJAisle'])['Quantity'].sum().reset_index()

		return s.to_json(orient='records')


class TaskList(Resource):
	def get(self):
		ingredientString = request.args['ingredient']
		ingredients = json.loads(ingredientString)

		# reverses list so first ingredients appear at the top
		ingredients.sort(key=lambda x: x['TJAisle'], reverse = True)

		mealsString = request.args['meals']
		meals = json.loads(mealsString)

		mealListString = ''
		for meal in meals:
			mealListString = mealListString + '(' + str(meal['Number']) + ') ' + meal['Meal']['MealName'] + ' '

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
				'title': ingredient['Ingredient'] + ' (' + str(ingredient['Quantity']) + ' ' + ingredient['Unit'] + ')'
			}

			# Add new task to the list that was previously created
			# only if quantity is greater than 0
			if ingredient['Quantity'] > 0:
				service.tasks().insert(tasklist=tasklist_id, body=task).execute()

		# Add the meals to the top of the list so we know we remember what we planned to make
		mealTask = {
			'title': mealListString
			}

		service.tasks().insert(tasklist=tasklist_id, body=mealTask).execute()
		
		return tasklist, 201

api.add_resource(Meals, '/meals')
api.add_resource(Ingredients, '/ingredients')
api.add_resource(TaskList, '/tasklist')
api.add_resource(AllIngredients, '/allingredients')
api.add_resource(MealList, '/meallist')