myApp.run([
    '$rootScope',
    '$state',
    '$location',
    '$localStorage',
    'Restangular',
    function($rootScope,
             $state,
             $location,
             $localStorage,
             Restangular) {

        // Restangular.setErrorInterceptor(function (response, deferred, responseHandler) {
        //     if (response.status === 401) {
        //         if ($state)
        //         return false; // error handled
        //     }
        //
        //     return true; // error not handled
        // });
        $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams){
            requireAuth = toState.resolve.requireAuth();
            if (requireAuth && !$localStorage.token) {
                event.preventDefault();
                $state.go('base.login');
            } else if (toState.name == 'base.login' && $localStorage.token) {
                event.preventDefault();
                $state.go('home');
            }
            // event.preventDefault();
        });

        if ($localStorage.token) {
            Restangular.setDefaultHeaders({Authorization: 'Bearer ' + $localStorage.token});
        }
}]);

myApp.constant('CLIENT_INFO', {
    'CLIENT_ID': 'rPoIgWgabADDBPjt7kdPFyGG8yaTensmkpzOGgn2',
    'CLIENT_SECRET': '1dJH9fgxexsBAuHY5vMenAK00tVQdYrmVu1N5xYes7XRApK4Rwnw86UFU75FxsUo2fMMGokm6zvlfVAjGjEg4rWl4ZeYeHiSbE341eXMrT7EOUYKBZxG4K2lk1Q3c7Bu',
});

myApp.constant('USER_ROLES', {
    'TEACHER': 'teacher',
    'MENTOR': 'mentor',
    'STUDENT': 'studnet'
});