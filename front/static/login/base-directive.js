angular.module("scienceFairForum").directive('baseDirective', function() {
    return {
        templateUrl: '/static/home/home.html',
        controller: ['$scope', '$state', 'User', function($scope, $state, User) {
            $scope.goHome = function() {
                $state.go("base.login");
            };
        }]
    }
});
