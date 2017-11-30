myApp.service('User', [
    'Request',
    'Restangular',
    '$localStorage',
    '$state',
    'USER_ROLES',
    function(Request,
             Restangular,
             $localStorage,
             $state,
             USER_ROLES) {

    user = {};
    user.userInfo = {};

    /**
     * Login user and get access token
     * @param {string} username
     * @param {string} password
     * @return {Object} Returns a restangular object
     */
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
                    $state.go('home.users', {userId: user.userInfo.id});
                });
            }
        }, function(error) {
            return error.status;
        });
    };


    /**
     * Logout user
     */
    user.logout = function() {
        user.userInfo = {};
        $localStorage.userInfo = undefined;
        $localStorage.token = undefined;
        Restangular.setDefaultHeaders({});
        $state.go('base.login');
    };

    /**
     * Get logged in user's information. If any error occurs, log out user
     * @return {Object} Returns a restangular object
     */
    user.getInfo = function() {
        return Request.me().then(function(response) {
            user.userInfo.username = response.username;
            user.userInfo.role = response.role;
            user.userInfo.id = response.id;
            $localStorage.userInfo = user.userInfo;
        }, function(error) {
            user.logout();
        })

    };

    /**
     * Check if logged in user is a teacher
     * @return {bool}
     */
    user.isTeacher = function() {
        return user.checkRole(USER_ROLES.TEACHER);
    };

    /**
     * Check if logged in user is a mentor
     * @return {bool}
     */
    user.isMentor = function() {
        return user.checkRole(USER_ROLES.MENTOR);
    };

    /**
     * Check if logged in user is a student
     * @return {bool}
     */
    user.isStudent = function() {
        return user.checkRole(USER_ROLES.STUDENT);
    };

    /**
     * Check if logged in user's role is equal to role
     * @param {string} role Role to check for
     * @return {bool}
     */
    user.checkRole = function(role) {
        if (user.userInfo === {}) {
            return False
        }
        return user.userInfo.role === role;
    };

    return user
}]);