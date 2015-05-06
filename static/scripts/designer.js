var DesignerApp = angular.module('DesignerApp', [])
.config(function($interpolateProvider) {
	  $interpolateProvider.startSymbol('{[');
	  $interpolateProvider.endSymbol(']}');
});

DesignerApp.controller('DesignerController', function($scope,$http) {
    $scope.field_types = ['text','textarea','file','radio','integer','select','checkbox'];
    $scope.fields=[];
    $scope.initialize = function(init){
    	if (init.fields)
    		$scope.fields = init.fields;
    	if (init.id)
    		$scope.id = init.id;
    	$scope.urls = init.urls;
    }
    $scope.save = function(){
    	console.log('posting: ',$scope.id, $scope.fields);
    	$http.post($scope.urls.update,{fields:$scope.fields})
    	.success(function(){alert('The form has been updated.')})
    	.error(function(){alert('There was an error updating the form.')});
    };
    $scope.addField = function(){
    	$scope.fields.push({});
    };
    $scope.test = function(){
    	console.log($scope.fields);
    }
    $scope.addOption = function(field){
    	if (!field.choices)
    		field.choices = [];
    	field.choices.push({});
    }
    $scope.removeOption = function(field,index){
    	field.choices.splice(index,1);
    }
    $scope.removeField = function(index){
    	if(confirm('Are you sure you want to remove this field?'))
    		$scope.fields.splice(index,1);
    }
  });