angular.module("scienceFairForum").directive('classroomPostDirective', function() {
    return {
        templateUrl: '/static/classroom/classroom-post/classroom-post.html',
        scope: {
            classroom: '=',
        },
        controller: [
            '$scope',
            '$stateParams',
            '$state',
            '$uibModal',
            'User',
            'Request',
            function(
                $scope,
                $stateParams,
                $state,
                $uibModal,
                User,
                Request
            ) {
                Request.getPost($stateParams.classroomId, $stateParams.postId).then(function(response) {
                    $scope.post = response.plain();
                    $scope.postLoaded = true;
                });

                $scope.createComment = function(comment) {
                    Request.createComment($stateParams.classroomId, $stateParams.postId, comment).then(function(response) {
                        $scope.post.comments.push(response.plain());
                    })
                };

                // /**
                //  * Create post for classroom (Students only)
                //  * @param {String} content The content of the post.
                //  */
                // $scope.createPost = function(title, content) {
                //     Request.createPost(title, content, $stateParams.classroomId).then(function(response) {
                //         $scope.classroom.posts.push(response.plain());
                //         $scope.cancelPostForm();
                //     }, function(error) {
                //         $scope.error = error.data;
                //     })
                // };
                //
                // /**
                //  * Open post creation form modal
                //  */
                // $scope.openPostForm = function () {
                //     $scope.modalInstance = $uibModal.open({
                //         animation: true,
                //         templateUrl: '/static/classroom/post-modal-form.html',
                //         scope: $scope,
                //         size: 'md',
                //     });
                // };
                //
                //
                // /**
                //  * Close post creation form modal
                //  */
                // $scope.cancelPostForm = function() {
                //     $scope.modalInstance.close(false);
                // };
            }]
    }
});
