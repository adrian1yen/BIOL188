var myApp = angular.module('scienceFairForum', [
    'ui.router',
    'ngStorage',
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
            console.log('rerouting');
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
                url:'/classrooms/{classroomId:int}',
                template: '<classroom-directive></classroom-directive>'
            });
    }
]);