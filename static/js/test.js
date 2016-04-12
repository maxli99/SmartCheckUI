app.controller('test', function($scope, $http) {
    $scope.hidden_pannel = true;
    $scope.form_disabled = false;
    $scope.submit_button = 'Test';
    $scope.formData = {};
    $scope.process_form = function() {
        $scope.form_disabled = true;
        $scope.submit_button = '<i class="icon-spinner icon-spin"></i>';
        $http({
            method : 'POST',
            data : $scope.formData,
        }).success(function(data) {
            $scope.result_data = data;
            $scope.hidden_pannel = false;
            $scope.form_disabled = false;
            $scope.submit_button = 'Test';
        });
    };
});

