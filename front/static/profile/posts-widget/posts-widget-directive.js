angular.module("scienceFairForum").directive('postsWidgetDirective', function() {
    return {
        templateUrl: '/static/profile/posts-widget/posts-widget.html',
        scope: {
            posts: '='
        },
        controller: ['$scope', '$state', '$stateParams', function($scope, $state, $stateParams) {
            $scope.showingAll = false;
            $scope.postsLimit = 5;

            $scope.toggleShow = function() {
                $scope.postsLimit = !$scope.showingAll ? $scope.posts.length : 5;
                $scope.showingAll = !$scope.showingAll;
            };

            $scope.goToPost = function(classroomId, postId) {
                $state.go('home.classrooms.posts', {classroomId: classroomId, postId: postId});
            }
        }]
    }
});
