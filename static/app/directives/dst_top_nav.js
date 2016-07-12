angular.module('chroma.directive', [])

.directive('dstTopNav', function() {

  return {
    controller: function($scope, $cookies, $rootScope, $location, SelfFactory) {
      $scope.user_first_name = $cookies.user_first_name;
      $scope.expand = false;

      $scope.ontreepage = $location.$$path === '/tree' ? true : false;
      $scope.onselfpage = $location.$$path === '/self' ? true : false;

      $scope.getBubbles = function () {
       // console.log("imingetRElatives")
        $rootScope.curPage = '/tree';
        clearInterval($rootScope.globeSpin);
        $scope.ontreepage = true;
        $scope.onselfpage = false;
        if($location.$$path === '/self'){
          $rootScope.transitionToPool();
        } else {
          $location.path('/tree')
        }
      };
    },
    templateUrl: '../static/app/directives/dst_top_nav.html'
  };

});