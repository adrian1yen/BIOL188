angular.module("scienceFairForum").directive('classroomsWidgetDirective', function() {
    return {
        templateUrl: '/static/profile/classrooms-widget/classrooms-widget.html',
        scope: {
            classrooms: '='
        },
        controller: ['$scope', '$state', 'User', function($scope, $state, User) {
            $scope.goToClassroom = function(classroomId) {
                $state.go('home.classrooms', {classroomId: classroomId});
            }
        }]
    }
});
