'use strict';

var services;
services = angular.module('lmfeedb.services',[]);

services.factory('AuthenticationService', function() {
    var auth = {
        isLogged: false,
        login: '',
        token: ''
    };
    return auth;
});
