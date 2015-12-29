var vanellope = angular.module("auth", []);

// Template Symbols
vanellope.config(['$interpolateProvider', function($interpolateProvider) {
  /* Redefine template symbol */
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
}]);

vanellope.controller('loginCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.login = function() {
    $http.post('/login', {
      pwd: $scope.pwd
    }).then(function success(data) {
      window.location.href = '/';
    }, function error(data) {
    });
  };
}]);
