angular.module('chroma.chromosomes', [])

.controller('SelfController', [ '$scope', '$cookies', '$location', 'SelfFactory', 'd3Service', '$rootScope', function ($scope, $cookies, $location, SelfFactory, d3Service, $rootScope) {
   

  $scope.outcomes = $scope.outcomes || [];

  $scope.current = {};
 
  $scope.whichView = whichView;


  var whichView = function() {
    $rootScope.view = $location.$$path;
  };

  whichView();

  $rootScope.removeHelix = function () {

    d3.select("svg#vis").remove();
  };

  $rootScope.$watch(function () {
      return location.hash;
  }, function (value) {
     if($location.$$path === '/self'){
      console.log("PATH SELF")


       $('svg.datamap').remove();
     } else if($location.$$path === '/tree'){

       d3.select("svg#helix").remove();
     }
  });




var counter = 0;

  $scope.generateData = generateData;

  function generateData() {
   
    counter++;
    // Creating a range of numX (set to outcomes length) and then map
   var data =  d3.range(numX).map(function (d, i) {

  
        return [{
                    title: $scope.outcomes[d].title,
                    rsid: $scope.outcomes[d].rsid,
                    pair: $scope.outcomes[d].pair,
                    outcome: $scope.outcomes[d].outcome,
                   r: $scope.outcomes[d].r


              
                
                  }];
               
        });
    
      return data;
  }


  var exit = false;

  $scope.draw = draw;

  function draw () {
    if(exit) {
      return;
    }
  
    // below statement is whats giving all the gs/images the data attributes
    var cont = d3.selectAll("g#click").data(generateData())
   
   
    cont.each(function (d, index) {
    
      d3.select(this)
        .selectAll("image#click")
        .data(d)
        .attr("title", function (d){ return d.title; })
        .attr("rsid", function(d){ return d.rsid; })
        .attr("pair", function(d){ return d.pair; })
        .attr("outcome", function(d){ return d.outcome; })
     


        .on('click', function(d,i){

          console.log("title", d.title)
    
         $scope.$apply($scope.current = { title: d.title, rsid: d.rsid, pair: d.pair, outcome: d.outcome });
//           
        })
   })

}
  SelfFactory.getSnps($cookies.user_profile_id).then(function (outcomes) {
    $scope.allOutcomes = outcomes; //for testing purposes only

    for (var key in outcomes) {
      $scope.outcomes.push(outcomes[key]);
    }

    numX = $scope.outcomes.length;

   draw();
  });

//------------------------
 
  

  $rootScope.IntroOptions = {
      steps:[
         
        {
          intro:"Welcome to Genma!"
        },
        {
          intro:"SNPs can generate biological variation between people by causing differences in the recipes for proteins that are written in genes. Those differences can in turn influence a variety of health-related traits including disease susceptibility, or response to drugs"
        },
       
        {
          intro: "Click your chromosomes to find out what health risks you are susceptible to"
        }


        ],
  
      showStepNumbers: false,
      exitOnOverlayClick: true,
      exitOnEsc:true,
      doneLabel: 'Thanks'
  };

  var remove = function() {
    $('div.dna-info').remove();
    d3.select("#openg")
      .attr("width", 3000);

    d3.selectAll("image")
      .transition()
      .duration(2000)
     
   };
  
   //Calls the remove function, and sets a timeout to transition the user to the pool
   //page after the helix has collapsed and been removed from the page.
  $rootScope.transitionToPool = function(){
    exit = true;
    remove();
    setTimeout(function(){
      $scope.$apply($location.path('/bubblechart'));
      $rootScope.removeHelix();}, 500);
  };
}])
.factory('SelfFactory', function ($http) {

  var getSnps = function (userId) {
      return $http({
      method: 'POST',
      url: '/user/snpinfo/',
      data: userId
    }).then(function (snps) {

      return snps.data.outcomes;

    }).catch(function (err) {
      console.error('An error occured retreiving your SNPs ', err);
    });
  };

  return {
    getSnps: getSnps
  };
});


