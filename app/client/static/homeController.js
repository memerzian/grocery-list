(function () {
  'use strict';

  angular.module('DinnerPlansApp')

  .controller('homeController', function($scope, $http) {
  		$scope.mealNumber;
  		$scope.mealChoice;
  		$scope.ingredients = [];
  		$scope.mealPlans = [];
  		$scope.mealNumberOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  		getMealOptions();

  		function getMealOptions() {
			$http.get('http://localhost:5000/api/meals')
		  		.then(function(response) {
					  $scope.mealOptions = response.data;
		  		});
	  	};

	  	$scope.getIngredients = function() {
	  		var mealsArray = $scope.mealPlans.map(function(mp) {return mp.Meal;});
	  		var mealNameArray = mealsArray.map(function(m) {return m.MealName;});
	 
			$http.get('http://localhost:5000/api/ingredientsformeals',
			{
				params: {meals: JSON.stringify(mealNameArray)}
			})
		  		.then(function(response) {
		  			var data = response.data;
		  			$scope.ingredients = $scope.ingredients.concat(data);
		  		});
	  	};

	  	$scope.updateMealPlan = function() {
	  		$scope.mealPlans = [];
	  		var i;
			for (i = 0; i < $scope.mealNumber; i++) { 
			  var mealPlan = {Number: i + 1, Meal:""};
			  $scope.mealPlans.push(mealPlan);
			}
	  	}

	  	$scope.createTaskList = function() {
		  	$http.get('http://localhost:5000/api/tasklist',
			{
				params: {ingredient: JSON.stringify($scope.ingredients), meals: JSON.stringify($scope.mealPlans) }
			})
		  		.then(function(response) {
		  			
		  		});
	  	};

	  	$scope.addIngredient = function() {
	  		var newIngredient = {
		        TJAisle:  0,
		        Ingredient: 'New',
		        Quantity: 1,
		        Unit: ''
      		};

      		$scope.ingredients.push(newIngredient);
	  	}

	  	$scope.deleteIngredient = function(ingredient) {
	  		$scope.ingredients = $scope.ingredients.filter(i => i.$$hashKey !== ingredient.$$hashKey);
	  	}

	  	$scope.clearList = function() {
	  		$scope.ingredients = [];
	  	}

	  	$scope.ingredientsExist = function() {
	  		return $scope.ingredients.length == 0;
	  	}

	  	$scope.mealNumberArray = function() {
			return Array.apply(null, {length: $scope.mealNumber}).map(Number.call, Number)
	  	}
	});

}());