var DesignerApp = angular.module('DesignerApp', [])
.config(function($interpolateProvider) {
	  $interpolateProvider.startSymbol('{[');
	  $interpolateProvider.endSymbol(']}');
});

DesignerApp.controller('DesignerController', function($scope,$http) {
    $scope.field_types = [
                          {'class':'field','type':'text', 'label': 'Text Field'},
                          {'class':'field','type':'textarea', 'label': 'TextArea Field'},
                          {'class':'field','type':'file', 'label': 'File Field'},
                          {'class':'field','type':'radio', 'label': 'Radio Field'},
                          {'class':'field','type':'integer', 'label': 'Integer Field'},
                          {'class':'field','type':'select', 'label': 'Select Field'},
                          {'class':'field','type':'checkbox', 'label': 'Checkbox Field'},
                          {'class':'layout','type':'layout_html', 'label': 'HTML Label'}
                          ];
    
    $scope.fields=[];
    $scope.initialize = function(init){
    	if (init.fields)
    		$scope.fields = init.fields;
    	if (init.id)
    		$scope.id = init.id;
    	$scope.urls = init.urls;
    };
    $scope.move = function(index,diff){
    	$scope.fields.splice(index+diff, 0, angular.copy($scope.fields.splice(index, 1)[0]));
    };
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