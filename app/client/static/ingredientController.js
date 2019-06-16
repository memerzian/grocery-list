(function () {
  'use strict';

  angular.module('DinnerPlansApp')

  .controller('ingredientController', function($scope, $http) {
  	getDistinctIngredients();
  	$scope.ingredients;
  	$scope.selectedIngredient;
  	$scope.mealList;
	
	function getDistinctIngredients() {
			$http.get(config.apiUrl + '/ingredients')
		  		.then(function(response) {
		  			$scope.ingredients = response.data; 
		  		});
	  	};

	$scope.getMealList = function(selectedIngredient) {
		$http.get(config.apiUrl + '/meallist',
		{
			params: {ingredient: selectedIngredient.id}
		})
	  		.then(function(response) {
				  $scope.mealList = response.data;
	  		});
  	};

	});

}());