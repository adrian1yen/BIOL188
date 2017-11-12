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
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('home', {
                url:'/',
                templateUrl: '/static/home/home.html',
                resolve: {
                    'requireAuth': function() { return true }
                }
            })
            .state('base', {
                abstract: true,
                templateUrl: 'static/login/base.html',
            })
            .state('base.login', {
                url:'/login',
                template:'<login-directive></login-directive>',
                resolve: {
                    'requireAuth': function() { return false }
                }
            })
            .state('base.register', {
                url:'/register',
                template:'<register-directive></register-directive>',
                resolve: {
                    'requireAuth': function() { return false }
                }
            });
    }
]);