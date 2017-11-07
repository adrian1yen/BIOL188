angular.module("scienceFairForum").directive('loginDirective', function() {
    return {
        templateUrl: '/static/login/login.html',
        controller: ['$scope', 'User', function($scope, User) {
            $scope.login = function(username, password) {
                User.login(username, password);
            }
        }]
    }
});