angular.module("scienceFairForum").directive('homeDirective', function() {
    return {
        templateUrl: '/static/home/home.html',
        controller: ['$scope', '$stateParams', '$state', 'User', 'Request', function($scope, $stateParams, $state, User, Request) {
            $scope.currentUser = User.userInfo;

            $scope.goHome = function() {
                $state.go('home.users', {userId: User.userInfo.id})
            };

            $scope.logout = function() {
                User.logout();
            }
        }]
    }
});
