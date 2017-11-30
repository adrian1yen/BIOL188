angular.module("scienceFairForum").directive('classroomDirective', function() {
    return {
        templateUrl: '/static/classroom/classroom.html',
        scope: {
            classroom: '=',
        },
        controller: ['$scope', 'User', function($scope, User) {$scope.User = User;}]
    }
});
