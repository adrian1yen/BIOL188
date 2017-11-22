myApp.run([
    '$rootScope',
    '$state',
    '$location',
    '$localStorage',
    'Restangular',
    'User',
    function($rootScope,
             $state,
             $location,
             $localStorage,
             Restangular,
             User) {

        $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams){
            requireAuth = toState.data.requireAuth;
            if (requireAuth && !$localStorage.token) {
                event.preventDefault();
                $state.go('base.login');
            } else if (!requireAuth && $localStorage.token) {
                event.preventDefault();
                User.getInfo().then(function() {
                    $state.go('home.users', {userId: User.userInfo.id});
                });
            }
        });

        if ($localStorage.token) {
            Restangular.setDefaultHeaders({Authorization: 'Bearer ' + $localStorage.token});
        }
}]);

myApp.constant('USER_ROLES', {
    'TEACHER': 'teacher',
    'MENTOR': 'mentor',
    'STUDENT': 'studnet'
});