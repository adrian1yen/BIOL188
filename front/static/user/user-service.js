myApp.service('User', [
    'Request',
    'Restangular',
    '$localStorage',
    '$state',
    function(Request,
             Restangular,
             $localStorage,
             $state) {

    user = {};
    user.userInfo = {};

    user.login = function(username, password) {
        console.log('logging in');
        return Request.login(username, password).then(function(response) {
            if (response.access_token) {
                user.userInfo.token = response.access_token;
                $localStorage.token = response.access_token;
                Restangular.setDefaultHeaders({Authorization: 'Bearer ' + $localStorage.token});
                return Request.me().then(function(response) {
                    user.userInfo.username = response.username;
                    user.userInfo.role = response.role;
                    user.userInfo.id = response.id;
                    $localStorage.userInfo = user.userInfo;
                    $state.go('home');
                });
            }
        }, function(error) {
            return error.status;
        });
    };

    user.getInfo = function() {
        Request.me().then(function(response) {
            user.userInfo.username = response.username;
            user.userInfo.role = response.role;
            user.userInfo.id = response.id;
            $localStorage.userInfo = user.userInfo;
            $state.go('home');
        })

    };

    return user
}]);