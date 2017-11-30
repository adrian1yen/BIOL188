angular.module("scienceFairForum").directive('commentsWidgetDirective', function() {
    return {
        templateUrl: '/static/profile/comments-widget/comments-widget.html',
        scope: {
            comments: '='
        },
        controller: ['$scope', '$state', function($scope, $state) {
            $scope.showingAll = false;
            $scope.commentLimit = 5;

            $scope.toggleShow = function() {
                $scope.commentLimit = !$scope.showingAll ? $scope.comments.length : 5;
                $scope.showingAll = !$scope.showingAll;
            };

            $scope.goToPost = function(postId) {
                $state.go('home.classrooms.posts', {postId: postId});
            }
        }]
    }
});
