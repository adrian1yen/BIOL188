angular.module("scienceFairForum").directive('classroomOverviewDirective', function() {
    return {
        templateUrl: '/static/classroom/classroom-overview/classroom-overview.html',
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
                $scope.User = User;

                Request.getClassroom($stateParams.classroomId).then(function(response) {
                    $scope.classroom = response.plain();
                    $scope.classroomLoaded = true;
                });

                /**
                 * Create post for classroom (Students only)
                 * @param {String} title The title of the post.
                 * @param {String} content The content of the post.
                 */
                $scope.createPost = function(title, content) {
                    Request.createPost(title, content, $stateParams.classroomId).then(function(response) {
                        $scope.classroom.posts.push(response.plain());
                        $scope.cancelPostForm();
                    }, function(error) {
                        $scope.error = error.data;
                    })
                };

                /**
                 * Open post creation form modal
                 */
                $scope.openPostForm = function () {
                    $scope.modalInstance = $uibModal.open({
                        animation: true,
                        templateUrl: '/static/classroom/post-modal-form.html',
                        scope: $scope,
                        size: 'md',
                    });
                };


                /**
                 * Close post creation form modal
                 */
                $scope.cancelPostForm = function() {
                    $scope.modalInstance.close(false);
                };
            }]
    }
});
