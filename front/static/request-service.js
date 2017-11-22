myApp.service('Request', function(Restangular, CLIENT_INFO) {
    request = {};
    api = Restangular.all('api');


    //~~~~~~~~~~~~~~~~~
    // User Endpoints
    //~~~~~~~~~~~~~~~~~

    // Authentication
    request.login = function(username, password) {
        return Restangular.all('auth').all('token').post({
            username: username,
            password: password,
            client_id: CLIENT_INFO.CLIENT_ID,
            client_secret: CLIENT_INFO.CLIENT_SECRET,
            grant_type: 'password'
        });
        // return Restangular.one('auth').one('token').get()
    };

    // Registration
    request.register = function(username, password, role) {
        return api.all('users').post({
            username:username,
            password:password,
            role:role
        });
    };

    // Logged in user information
    request.me = function() {
        return api.one('me').get();
    };


    //~~~~~~~~~~~~~~~~
    // User Endpoints
    //~~~~~~~~~~~~~~~~

    // Get user profile information
    request.getUserProfile = function(userId) {
        return api.one('users', userId).get()
    };


    //~~~~~~~~~~~~~~~~
    // Post Endpoints
    //~~~~~~~~~~~~~~~~

    // Create post for classroom
    request.createPost = function(data) {
        return api.all('posts').post(data);
    };

    return request
});