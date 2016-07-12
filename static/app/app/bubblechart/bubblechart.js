angular.module('chroma.bubblechart', [])
.controller('TreeController', [ '$scope', '$cookies', '$location', 'TreeFactory', 'd3Service', '$rootScope', function ($scope, $cookies, $location, TreeFactory, d3Service, $rootScope) {

  $scope.outcomes = $scope.outcomes || [];
  $scope.current = {};
 

  $scope.whichView = whichView;

  var whichView = function() {
    $rootScope.view = $location.$$path;
  };

  whichView();

  $rootScope.removeBubble = function () {

    d3.select("svg.bubble").remove();
  };

  $rootScope.showTree = function(){
    clearInterval($rootScope.globeSpin);
    $rootScope.killGlobe();
    $rootScope.curPage = '/bubblechart';
    $location.path('/bubblechart/');
  };

 


///----------------------
//var numX = 30
 var diameter = 700,
    format = d3.format(",d"),
    color = d3.scale.category20c();

var bubble = d3.layout.pack()
    .sort(null)
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select(".BodyContainer").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

//-----------------------------------

var dobj=[];

   
  $scope.generateData = generateData;

  function generateData() {
   // counter++;
    // Creating a range of numX (set to outcomes length) and then map
     var data = d3.range(numX).map(function (d, i) {
      //console.log(d)
       // var t = d * torsion - speed * counter;
         return [{ 
                    title: $scope.outcomes[d].title,
                    rsid: $scope.outcomes[d].rsid,
                    pair: $scope.outcomes[d].pair,
                    outcome: $scope.outcomes[d].outcome,
                    r: $scope.outcomes[d].r,
                    healthtip: $scope.outcomes[d].healthtip
                 
                  }];
                  
        });
     return data
     
   
      }




 var exit = false;

  $scope.draw = draw;

  function draw () {
    if(exit) {
      return;
    }
  
  // var nodes = bubble.nodes(generateData());

  //console.log("SCOPE", $scope.outcomes)
    for (var di=0;di<$scope.outcomes.length;di++) {
        // value is r or impact and determines size of bubble
      dobj.push({"key":di,"value":$scope.outcomes[di].r, 'title': $scope.outcomes[di].title, 'healthtip':$scope.outcomes[di].healthtip});
    }

    console.log("dobj", dobj)

    // var force = d3.layout.force()
    // .nodes(dobj)
    // .size([width, height])
    // .friction(0.9)
    // .charge(-70)
    // .gravity(0.07)
    // .theta(0.8)
    // .alpha(0.1)
    // .on("tick", tick)
    // .start();

    display_pack({children: dobj});
 

    function display_pack(root) {
        console.log("root2", root)
        var node = svg.selectAll(".node")
            .data(bubble.nodes(root)
            .filter(function(d) { return !d.children }))
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
             .style("fill", function(d) { 
                                        //color is based on ethnicity
                                      return color(d.r) })
             .attr("title", function (d){ return d.title; })
             //.attr("healthtip", function (d) {return d. healthtip;})
  
           .on('click', function(d,i){

          console.log("d", d)
   
     $scope.$apply($scope.current = { healthtip: d.healthtip});
           
        })

             .on("mouseover", function(d) {
              console.log("d", d, d.key)
                d3.select(this).style("fill", "gold"); 
                showToolTip(" "+[d.title]+" ",d.x+d3.mouse(this)[0]+50,d.y+d3.mouse(this)[1],true);
                //console.log(d3.mouse(this));
            })
            // .on("mousemove", function(d,i) {
            //     tooltipDivID.css({top:d.y+d3.mouse(this)[1],left:d.x+d3.mouse(this)[0]+50});
            // })    
            .on("mouseout", function() {
        d3.select(this).style("fill", function(d) { return color([d.r]); });
        showToolTip(" ",0,0,false);
      });






      node.append("circle")
          .attr("r", function(d) { return d.r })
           .attr("title", function (d){ return d.title; })
        .attr("rsid", function(d){ return d.rsid; })
        .attr("pair", function(d){ return d.pair; })
        .attr("outcome", function(d){ return d.outcome; })
        .attr("healthtip", function(d) { return d.healthtip; })

       // .call(force.drag)
          .on('click', function(d,i){

          console.log("d", d)

      $scope.$apply($scope.current = { healthtip: d.healthtip});
           console.log("onclick", $scope.current)
        })



      node.append("text")
          .attr("dy", ".3em")
          .style("text-anchor", "middle")
          .style("fill","black")
          .text(function(d) { return d.title });




    //-------------------------------
    
    }


     
  }

  function showToolTip(pMessage,pX,pY,pShow)
  {
    if (typeof(tooltipDivID)==="undefined") {
    tooltipDivID =$('<div id="messageToolTipDiv" style="position:absolute;display:block;z-index:10000;border:2px solid black;background-color:rgba(0,0,0,0.8);margin:auto;padding:3px 5px 3px 5px;color:white;font-size:12px;font-family:arial;border-radius: 5px;vertical-align: middle;text-align: center;min-width:50px;overflow:auto;"></div>');

    $('body').append(tooltipDivID);
    }
    if (!pShow) { tooltipDivID.hide(); return;}
    //MT.tooltipDivID.empty().append(pMessage);
    tooltipDivID.html(pMessage);
    tooltipDivID.css({top:pY,left:pX});
    tooltipDivID.show();
  }
  





TreeFactory.getSnps($cookies.user_profile_id).then(function (outcomes) {
    $scope.allOutcomes = outcomes; //for testing purposes only

    for (var key in outcomes) {
      $scope.outcomes.push(outcomes[key]);
    }

    


    numX = $scope.outcomes.length;
  

 draw();
  });


  $rootScope.IntroOptions = {
      steps:[{
          intro: "Welcome to your health bubble chart. The bigger bubbles represent health risks you are more suscpetible to. Click on those bubbles for tips on how to manage these health risks"
        }
    
      
      ],
      showStepNumbers: false,
      exitOnOverlayClick: true,
      exitOnEsc:true,
      nextLabel: '<strong><span style="color:green">Next</span></strong>',
      prevLabel: '<span style="color:red">Previous</span>',
      skipLabel: 'Exit',
      doneLabel: 'Thanks'
  };
  var remove = function() {
    $('div.dna-info2').remove();
    d3.select("svg.bubble")
      .attr("width", 3000);

   


    d3.selectAll("image")
      .transition()
      .duration(2000)
    
   };
  
  $rootScope.transitionToBool = function(){
    exit = true;
    remove();
    setTimeout(function(){
      $scope.$apply($location.path('/chromosomes'));
      $rootScope.removeBubble();}, 500);
  };
}])



       

.factory('TreeFactory', function ($http) {

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

//       