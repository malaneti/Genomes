angular.module('chroma.auth', ['ngCookies', 'ngRoute'])

.controller('AuthController', function($http, $scope, $rootScope, $cookies, $location, $rootElement, $timeout, $window, AuthFactory) {
  $scope.user = {};

  $rootScope.signOut = function() {
    AuthFactory.signOut();
  };

})
.factory('AuthFactory', function($http, $cookies, $location) {

  var isAuth = function () {
    return $cookies['token'];
  };

  var signOut = function() {
    delete $cookies['token'];
    delete $cookies['user_first_name']
    window.location.href = '/';
  };

  return {
    signOut: signOut,
    isAuth: isAuth
  };
});