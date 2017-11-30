var myApp = angular.module('scienceFairForum', [
    'ui.router',
    'ngStorage',
    'ui.bootstrap',
    'restangular']);

myApp.config([
    '$interpolateProvider',
    '$stateProvider',
    '$urlRouterProvider',
    '$locationProvider',
    'RestangularProvider',
    function (
        $interpolateProvider,
        $stateProvider,
        $urlRouterProvider,
        $locationProvider,
        RestangularProvider) {

        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        RestangularProvider.setRequestSuffix("/");
        // RestangularProvider.setDefaultHttpFields({'X-CSRFToken': Cookies.get('csrftoken')});


        // Routing
        $urlRouterProvider.otherwise(function($injector, $location) {
            $injector.invoke(['$state', 'User', function($state, User){
                if (!User.userInfo.id) {
                    User.getInfo().then(function() {
                        // If getInfo is successful go to profile else go to login
                        if (User.userInfo.id) {
                            $state.go('home.users', {userId: User.userInfo.id});
                        } else {
                            $state.go('base.login');
                        }
                    })
                } else {
                    $state.go('home.users', {userId: User.userInfo.id});
                }
            }]);
        });
        $stateProvider
            .state('base', {
                abstract: true,
                template: '<base-directive></base-directive>',
                data: {
                    'requireAuth': false
                }
            })
            .state('base.login', {
                url:'/login',
                template:'<login-directive></login-directive>',
            })
            .state('base.register', {
                url:'/register',
                template:'<register-directive></register-directive>',
            })
            .state('home', {
                abstract: true,
                template: '<home-directive></home-directive>',
                data: {
                    'requireAuth': true
                },
                resolve: {
                    'User': function(User) {
                        return User.getInfo();
                    }
                }
            })
            .state('home.users', {
                url: '/users/{userId:int}',
                template: '<profile-directive></profile-directive>'
            })
            .state('home.classrooms', {
                abstract: true,
                url:'/classrooms/{classroomId:int}',
                template: '<classroom-directive classroom="classroom"></classroom-directive>',
                resolve: {
                    'classroom': function(Request, $stateParams) {
                        return Request.getClassroom($stateParams.classroomId).then(function(response) {
                            return response.plain();
                        });
                    }
                },
                controller: function($scope, classroom) {
                    $scope.classroom = classroom;
                }
            })
            .state('home.classrooms.overview', {
                url: '/overview',
                template: '<classroom-overview-directive classroom="classroom"></classroom-overview-directive>',
                controller: function($scope, classroom) {
                    $scope.classroom = classroom;
                }
            })
            .state('home.classrooms.posts', {
                url: '/posts/{postId:int}',
                template: '<classroom-post-directive classroom="classroom"></classroom-post-directive>',
                controller: function($scope, classroom) {
                    $scope.classroom = classroom;
                }
            });
    }
]);