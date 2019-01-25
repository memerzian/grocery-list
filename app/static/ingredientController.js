(function () {
  'use strict';

  angular.module('DinnerPlansApp')

  .controller('ingredientController', function($scope, $http) {
  	getDistinctIngredients();
  	$scope.ingredients;
  	$scope.selectedIngredient;
  	$scope.mealList;
	
	function getDistinctIngredients() {
			$http.get('http://localhost:5000/allingredients')
		  		.then(function(response) {
		  			//The json comes through as a string if the parse is not included
		  			$scope.ingredients = JSON.parse(response.data); 
		  		});
	  	};

	$scope.getMealList = function(selectedIngredient) {
		$http.get('http://localhost:5000/meallist',
		{
			params: {ingredient: selectedIngredient}
		})
	  		.then(function(response) {
	  			$scope.mealList = JSON.parse(response.data);
	  		});
  	};

	});

   

}());