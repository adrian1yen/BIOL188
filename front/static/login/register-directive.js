angular.module("scienceFairForum").directive('registerDirective', function() {
    return {
        templateUrl: '/static/login/register.html',
        controller: ['$scope', '$state', 'Request', 'USER_ROLES', function($scope, $state, Request, USER_ROLES) {
            $scope.USER_ROLES = USER_ROLES;

            $scope.register = function(username, password, role) {
                Request.register(username, password, role).then(function() {
                    $state.go('base.login');
                }, function(error) {
                    if (error.status === 400) {
                        $scope.error = error.data;
                    } else {
                        $scope.error = 'Something went wrong. Please try again or contact support.';
                    }
                })
            }
        }]
    }
});
