angular.module("scienceFairForum").directive('loginDirective', function() {
    return {
        templateUrl: '/static/login/login.html',
        controller: ['$scope', '$state', 'User', function($scope, $state, User) {
            $scope.login = function(username, password) {
                User.login(username, password).then(function(error_status) {
                    if (error_status === 401) {
                        console.log('Unauthorized');
                    } else if (error_status === 400) {
                        console.log('Bad');
                    } else {
                        console.log('Else');
                    }
                });
            }

            $scope.goToRegister = function() {
                $state.go('base.register');
            }
        }]
    }
});