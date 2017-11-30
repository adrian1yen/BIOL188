myApp.service('Request', function($localStorage, Restangular, CLIENT_INFO) {
    request = {};
    api = Restangular.all('api');


    //~~~~~~~~~~~~~~~~~
    // User Endpoints
    //~~~~~~~~~~~~~~~~~

    /**
     * Login and authenticate user
     * @param {string} username
     * @param {string} password
     * @return {Object} Returns a restangular object
     */
    request.login = function(username, password) {
        return Restangular.all('auth').all('token').post({
            username: username,
            password: password,
            client_id: CLIENT_INFO.CLIENT_ID,
            client_secret: CLIENT_INFO.CLIENT_SECRET,
            grant_type: 'password'
        });
    };

    /**
     * Creates a new user
     * @param {string} username
     * @param {string} password
     * @param {string} role Role of the user (Teacher, Mentor, Student)
     * @return {Object} Returns a restangular object
     */
    request.register = function(username, password, role) {
        return api.all('users').post({
            username:username,
            password:password,
            role:role
        });
    };

    /**
     * Get logged in user's information
     * @return {Object} Returns a restangular object
     */
    request.me = function() {
        return api.one('me').get();
    };


    //~~~~~~~~~~~~~~~~
    // User Endpoints
    //~~~~~~~~~~~~~~~~

    /**
     * Get a certain users information. Includes username, role, posts, comments, etc.
     * @param {int} userId The user id of the selected user
     * @return {Object} Returns a restangular object
     */
    request.getUserProfile = function(userId) {
        return api.one('users', userId).get()
    };

    request.addClassroom = function(code) {
        return api.one('users', $localStorage.userInfo.id).all('add_class').post({code: code});
    };


    //~~~~~~~~~~~~~~~~
    // Post Endpoints
    //~~~~~~~~~~~~~~~~

    /**
     * Create a post for a certain classroom (Students only)
     * @param {string} title The title for the post
     * @param {string} content The content for the post
     * @param {string} classroomId The id of the classroom the post is for
     * @return {Object} Returns a restangular object
     */
    request.createPost = function(title, content, classroomId) {
        return api.one('classrooms', classroomId).all('posts').post({title: title, content: content});
    };

    /**
     * Get post with postId
     * @param {int} postId Id of post to get
     * @return {Object} Returns a restangular object
     */
    request.getPost = function(classroomId, postId) {
        return api.one('classrooms', classroomId).one('posts', postId).get();
    };


    //~~~~~~~~~~~~~~~~
    // Post Endpoints
    //~~~~~~~~~~~~~~~~

    /**
     * Create a comment for post
     * @param {int} postId
     * @param {string} comment
     * @return {Object} Returns a restangular object
     */
    request.createComment = function(classroomId, postId, content) {
        return api.one('classrooms', classroomId).one('posts', postId).all('comments').post({content: content, postId: postId});
    };


    //~~~~~~~~~~~~~~~~~~~~~~
    // Classroom Endpoints
    //~~~~~~~~~~~~~~~~~~~~~~

    /**
     * Get classroom information by classroomId
     * @param {int} classroomId Id of classroom to be retrieved
     * @return {Object} Returns a restangular object
     */
    request.getClassroom = function(classroomId) {
        return api.one('classrooms', classroomId).get();
    };

    /**
     * Create classroom with teacher = logged in user
     * @param {string} name Name of classroom to be created
     * @return {Object} Returns a restangular object
     */
    request.createClassroom = function(name) {
        return api.all('classrooms').post({name:name});
    };

    return request
});