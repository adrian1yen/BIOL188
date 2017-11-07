myApp.service('Authentication', function($http , $localStorage, $state, $rootScope, Request) {
    var service = {};

    service.logout = logout;


    service.login = function(username, password) {
        console.log('logging in');
        Request.login(username, password).then(function (response) {
            if (response.token) {
                var token = response.token;
                Request.me(token).then(function(response) {
                    console.log(response);
                    // var id = response[0].id;
                    // $localStorage.currentUser = {username:username, id:id, token:token};
                    // $rootScope.currentUser = $localStorage.currentUser;
                    // Rest.setDefaultHeaders({Authorization: 'Bearer ' + $localStorage.user.userInfo.token});
                    // $state.go('home');

                }, function(error) {
                    console.log(error);
                });
            }
        }, function (error) {
            console.log('error');
            console.log(error);
        })
    };

    function logout() {
        delete $localStorage.currentUser;
        delete $rootScope.currentUser;
        $http.defaults.headers.common.Authorization = '';
    }
    return service;
});
