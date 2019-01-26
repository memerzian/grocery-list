'use strict';

var dinnerPlansApp = angular.module('DinnerPlansApp', ['ngRoute']);

dinnerPlansApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '../static/home.html',
        controller: 'homeController'
      }).
      when('/ingredient', {
        templateUrl: '../static/ingredient.html',
        controller: 'ingredientController'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);