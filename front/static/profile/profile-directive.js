angular.module("scienceFairForum").directive('profileDirective', function() {
    return {
        templateUrl: '/static/profile/profile.html',
        controller: [
            '$scope',
            '$stateParams',
            '$state',
            'User',
            'Request',
            'USER_ROLES',
            function($scope,
                     $stateParams,
                     $state,
                     User,
                     Request,
                     USER_ROLES) {
            Request.getUserProfile($stateParams.userId).then(function(response) {
                $scope.user = response.plain();
                $scope.classrooms = $scope.user.classrooms;
                $scope.comments = $scope.user.comments;
                $scope.userLoaded = true;
            });
        }]
    }
});
