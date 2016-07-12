angular.module('chroma.relatives', [])
.factory('Relatives', function($http){

  getRelatives = function(){
    return $http({
      method: 'GET',
      url: '/user/snpinfo/'
    })
  }

  return {
    getRelatives: getRelatives
  }
})



