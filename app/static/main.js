'use strict';

var dinnerPlansApp = angular.module('DinnerPlansApp', ['ngRoute']);

dinnerPlansApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '../static/views/home.html',
        controller: 'homeController'
      }).
      when('/ingredient', {
        templateUrl: '../static/views/ingredient.html',
        controller: 'ingredientController'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);