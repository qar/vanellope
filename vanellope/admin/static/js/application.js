var vanellope = angular.module("vanellope", []);

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


vanellope.controller('adminCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.configs = {};

  $http.get('/api/v1/configuration').then(function success(data) {
    $scope.configs = data.data.configs;
  }, function error(data) {
  });

  $scope.save = function() {
    $http.put('/api/v1/configuration', $scope.configs).then(function success(data) {
      window.location.reload();
    }, function error(data) {
    });
  };
}]);

vanellope.controller('editorCtrl', ['$scope', '$http', function($scope, $http) {
  var patt = /\/admin\/edit\/(\w{8})\+.*/;
  $scope.entry_id = undefined;
  var path = window.location.pathname;

  var editor = new Simditor({
    textarea: $('#editor'),
    upload: {
      url: '/api/v1/image',
      params: {
        // what key the response data should use to represent file path
        pathKey: 'file_path',

        ifsuccess: JSON.stringify({
          success: true
        }),

        iffail: JSON.stringify({
          success: false
        })
      },
      fileKey: 'image',
      connectionCount: 1,
      leaveConfirm: 'Uploading is in progress, are you sure to leave this page?'
    }
  });

  if (path.startsWith('/admin/edit') && path.match(patt)) {
    $scope.entry_id = path.match(patt)[1];

    $http.get('/api/v1/article/' + $scope.entry_id).then(function success(data) {
      $scope.post = data.data;
      $scope.title = data.data.title;
      $scope.content = data.data.content;
      $scope.category = data.data.category;
      $scope.state = data.data.state;

      if (Object.prototype.toString.call(data.data.tags) === '[object String]') {
        $scope.tags = data.data.tags;
      } else if (Object.prototype.toString.call(data.data.tags) === '[object Array]') {
        $scope.tags = data.data.tags.join(', ');
      } else {
        $scope.tags = '';
      }

      editor.setValue($scope.content);
    }, function error(data) {
    });
  } else {
    $scope.state = 'draft';
  }

  $scope.savePost = function() {
    var title = $scope.title;
    var content = editor.getValue();
    var category = $scope.category;
    var state = $scope.state;
    var tags;

    if (Object.prototype.toString.call($scope.tags) === '[object String]') {
      tags = $scope.tags.split(',');
    } else if (Object.prototype.toString.call($scope.tags) === '[object Array]') {
      tags = $scope.tags;
    } else {
      tags = [];
    }

    if ($scope.entry_id) {
      $http.put('/api/v1/posts', {
        title: title,
        uuid: $scope.entry_id,
        content: content,
        category: category,
        tags: tags,
        state: state
      }).then(function success(data) {
        window.location.href = data.data.url ? data.data.url : '/';
      }, function error(data) {
      });
    } else {
      $http.post('/api/v1/posts', {
        title: title,
        content: content,
        category: category,
        state: state,
        tags: tags
      }).then(function success(data) {
        window.location.href = data.data.url ? data.data.url : '/';
      }, function error(data) {
      });
    }
  };

  $scope.deletePost = function() {
    if ($scope.entry_id) {
      $http.delete('/api/v1/posts/' + $scope.entry_id).then(function success(data) {
        window.location.reload();
      }, function error(data) {
      });
    }
  };

}]);

vanellope.controller('trashCtrl', ['$scope', '$http', function($scope, $http) {
  console.log('trash controller active');
  $scope.dropEntry = function(entryID) {
    $http.delete('/api/v1/admin/trash/' + entryID).then(function success(data) {
      window.location.reload();
    });
  };
}]);

vanellope.controller('draftsCtrl', ['$scope', '$http', function($scope, $http) {
  console.log('drafts controller active');
  $scope.deleteEntry = function(entryID) {
    $http.delete('/api/v1/posts/' + entryID).then(function success(data) {
      window.location.reload();
    });
  };
}]);

