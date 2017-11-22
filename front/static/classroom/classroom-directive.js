angular.module("scienceFairForum").directive('classroomDirective', function() {
    return {
        templateUrl: '/static/classroom/classroom.html',
        controller: ['$scope', '$stateParams', '$state', 'User', 'Request', function($scope, $stateParams, $state, User, Request) {
            $scope.createPost = function(content) {
                data = {
                    content: content,
                    classroomId: $stateParams.classroomId
                };
                Request.createPost(data).then(function(response) {
                    console.log(response);
                }, function(error) {
                    console.log(error);
                })
            }
        }]
    }
});
