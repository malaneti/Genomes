var app = angular.module('chroma', [
  'chroma.bubblechart',
  'chroma.chromosomes',
  'ngRoute',
  'ngCookies',
  'chroma.d3Service',
  'chroma.auth',
  'chroma.directive',
  'ngMaterial',
  'angular-intro'
])

//. when is a method on $route
// $routeProvider used for configuring routes 
//$routeProvider is the key service which set the configuration of urls, 
//map them with the corresponding html page or ng-template, and attach a controller with the same.
.config(function ($routeProvider) {
 
  $routeProvider
     .when('/', {
      redirectTo: '/chromosomes'
    })
    .when('/signin', {
      templateUrl: '/maintemplates/index.html',
      controller: 'AuthController'
    })
    .when('/signout', {
      templateUrl: '/maintemplates/main.html',
      authenticate: true
    })
    .when('/self', {
      templateUrl: '/static/app/chromosomes/chromosomes.html',
      controller: 'SelfController',
      authenticate: true
    })
    .when('/tree', {
      templateUrl: '/static/app/bubblechart/bubblechart.html',
      controller: 'TreeController',
      authenticate: true
    })
    .otherwise({
      redirectTo : '/signin'
    });
})

.run(function($rootScope, $location, $cookies, AuthFactory){

  $rootScope.$on('$routeChangeStart', function(evt, next, current){
    if(next.$$route && next.$$route.authenticate && ! AuthFactory.isAuth()){
      $location.path('/signin');
    }
  });
});
