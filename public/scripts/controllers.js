'use strict';
var controllers;
controllers = angular.module('lmfeedb.controllers', []);
function getapiroot($location) {
  var lhost = $location.host();
  var lport = $location.port();
  return 'http://'+lhost+':'+lport;
}
function urlBase64Decode(str) {
  var output = str.replace('-', '+').replace('_', '/');
  switch (output.length % 4) {
    case 0:
      break;
    case 2:
      output += '==';
      break;
    case 3:
      output += '=';
      break;
    default:
      throw 'Illegal base64url string!';
  }
  return window.atob(output); //polifyll https://github.com/davidchambers/Base64.js
}
///////// controllers ///////////
controllers
.controller('LoginCtrl', ['$scope','$location','$window','AuthenticationService','$http',
    '$routeParams',function($scope,$location,$window,AuthenticationService,$http,$routeParams) {
        $scope.apiroot = getapiroot($location);
        $scope.user = {username:'',password:'',submit:''};
        $scope.error = '';
        $scope.submit = function () {
        if($scope.user.username !== undefined && $scope.user.password !== undefined) {
            var authdata = {
              "username": $scope.user.username,
              "password": $scope.user.password
            };
            $http.post(getapiroot($location) + '/auth', authdata)
            .then(function onSuccess(response) {
                var data = response.data;
                $scope.token = data["access_token"];
                if($scope.token) {
                    AuthenticationService.isLogged = true;
                    AuthenticationService.token = $scope.token;
                    $window.sessionStorage.token = $scope.token;
                    $window.sessionStorage.login = $scope.user.username;
                    $scope.error = '';
                    $location.path('/main');
                } else {
                    $scope.error = 'Error: Invalid user received from token';
                    AuthenticationService.isLogged = false;
                    delete $window.sessionStorage.token;
                    delete $window.sessionStorage.login;
                }
            })
            .catch(function onError(data) {
                AuthenticationService.isLogged = false;
                $scope.error = 'Error: Invalid user or password';
            });
        }
    };
}])
.controller('MainCtrl',['$scope', '$http', '$location', '$window', 'AuthenticationService', function($scope, $http, $location, $window, AuthenticationService) {
    $scope.user = {username:'username',password:'password',submit:''};
    $scope.apiroot = getapiroot($location);
    $scope.error = "";
    AuthenticationService.login = $window.sessionStorage.login;
    $scope.user.username = AuthenticationService.login;
    $scope.logout = function() {
        $scope.error = '';
        AuthenticationService.isLogged = false;
        delete $window.sessionStorage.token;
        $location.path('/');
    };
    $scope.setVibration = function(finger, frc, leng) {
      $http.post(getapiroot($location) + '/api/v1/start/'+finger+'/'+frc+'/'+leng)
      .then(function onSuccess(response) {
          var data = response.data;
          $scope.error = '';
          error_detected = false;
      });
    };
    $scope.clearVibration = function(finger) {
      $http.post(getapiroot($location) + '/api/v1/stop/'+finger)
      .then(function onSuccess(response) {
          var data = response.data;
          $scope.error = '';
          error_detected = false;
      });
    };
    $scope.starttest = function() {
      $http.post(getapiroot($location) + '/starttest')
      .then(function onSuccess(response) {
          var data = response.data;
          $scope.error = '';
          error_detected = false;
      });
    };
    $scope.stoptest = function() {
      $http.post(getapiroot($location) + '/stoptest')
      .then(function onSuccess(response) {
          var data = response.data;
          $scope.error = '';
          error_detected = false;
      });
    };
  }
]);
