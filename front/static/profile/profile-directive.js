angular.module("scienceFairForum").directive('profileDirective', function() {
    return {
        templateUrl: '/static/profile/profile.html',
        controller: [
            '$scope',
            '$stateParams',
            '$state',
            '$uibModal',
            'User',
            'USER_ROLES',
            'Request',
            function(
                $scope,
                $stateParams,
                $state,
                $uibModal,
                User,
                USER_ROLES,
                Request
            ) {
            $scope.User = User;
            $scope.USER_ROLES = USER_ROLES;

            Request.getUserProfile($stateParams.userId).then(function(response) {
                $scope.user = response.plain();
                $scope.classrooms = $scope.user.classrooms;
                $scope.comments = $scope.user.comments;
                $scope.posts = $scope.user.posts;
                $scope.userLoaded = true;
            });

            /**
             * Open add classroom form modal
             */
            $scope.openAddClassroom = function() {
                $scope.modalInstance = $uibModal.open({
                    animation: true,
                    templateUrl: "/static/profile/add-classroom-modal.html",
                    scope: $scope,
                    size: 'sm'
                })
            };


            /**
             * Add classroom to users classrooms and close modal
             * @param {string} code Classroom's code that is to be added to users classrooms
             */
            $scope.addClassroom = function(code) {
                Request.addClassroom(code).then(function(response) {
                    $scope.classrooms.push(response.plain());
                    $scope.closeModal();
                }, function(error) {
                    $scope.error = error.data;
                });
            };

            /**
             * Open create classroom form modal
             */
            $scope.openCreateClassroom = function() {
                $scope.modalInstance = $uibModal.open({
                    animation: true,
                    templateUrl: "/static/profile/create-classroom-modal.html",
                    scope: $scope,
                    size: 'md'
                })
            };

            /**
             * Create classroom. Only used by teachers
             * @param {string} name Classroom's name
             */
            $scope.createClassroom = function(name) {
                Request.createClassroom(name).then(function(response) {
                    $scope.classrooms.push(response.plain());
                    $scope.closeModal();
                }, function(error) {
                    $scope.error = error.data;
                });
            };

            /**
             * Close modals
             */
            $scope.closeModal = function() {
                $scope.modalInstance.close(false);
            }
        }]
    }
});
