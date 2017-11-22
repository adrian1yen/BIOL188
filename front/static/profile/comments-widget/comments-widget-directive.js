angular.module("scienceFairForum").directive('commentsWidgetDirective', function() {
    return {
        templateUrl: '/static/profile/comments-widget/comments-widget.html',
        scope: {
            comments: '='
        },
        controller: ['$scope', '$state', function($scope, $state) {
            $scope.comments = [
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title lkajsdflkjasflkjflajkf", content: "Some random comment that is important or somethinglkajsdlfkjalsfkjalfkjaslkfja laksjdf lkasdfj lkasdfj lkasdfj lsakjf lakfjd ."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
                {post_title: "Post Title", content: "Some random comment that is important or something."},
            ];

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
