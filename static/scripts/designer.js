var DesignerApp = angular.module('DesignerApp', [])
.config(function($interpolateProvider) {
	  $interpolateProvider.startSymbol('{[');
	  $interpolateProvider.endSymbol(']}');
});

DesignerApp.controller('DesignerController', function($scope) {
    $scope.field_types = ['text','textarea','file','radio','integer','select','checkbox'];
    $scope.fields=[];
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
  });