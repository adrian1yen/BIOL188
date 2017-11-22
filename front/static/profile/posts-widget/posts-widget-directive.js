angular.module("scienceFairForum").directive('postsWidgetDirective', function() {
    return {
        templateUrl: '/static/profile/posts-widget/posts-widget.html',
        scope: {
            posts: '='
        },
        controller: ['$scope', '$state', function($scope, $state) {
            $scope.posts = [
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title lkajsdflkjasflkjflajkf", content: "Some random comment that is important or somethinglkajsdlfkjalsfkjalfkjaslkfja laksjdf lkasdfj lkasdfj lkasdfj lsakjf lakfjd ."},
                {title: "Post Title", content: "Some random comment that is important or something."},
                {title: "Post Title", content: "Some random comment that is important or something."},
            ];

            $scope.showingAll = false;
            $scope.postsLimit = 5;

            $scope.toggleShow = function() {
                $scope.postsLimit = !$scope.showingAll ? $scope.posts.length : 5;
                $scope.showingAll = !$scope.showingAll;
            };

            $scope.goToPost = function(postId) {
                $state.go('home.classrooms.posts', {postId: postId});
            }
        }]
    }
});
