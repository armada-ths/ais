(function () {
    //Step counter set to 0
    let currentStep;

    //Sets the active form step depending on the number of clicks on the 'next' button
    var setActiveStep = function () {
        let formSteps = document.getElementsByClassName('form-step');
        for (let i = 0; i < formSteps.length; i++) {
            if (currentStep == i) {
                formSteps[i].setAttribute('id', 'activeStep');
                console.log(formSteps[i]);
            } else {
                formSteps[i].removeAttribute('id');
            }
        }
    }

    //Inits the form variables
    var initForm = function () {
        currentStep = 0;
        setActiveStep();
    }

    let nextButton = document.getElementById('next-step-btn');
    nextButton.addEventListener('click', function () {
        currentStep = currentStep + 1;
        console.log(currentStep);
        setActiveStep();
    })

    let backButton = document.getElementById('back-step-btn');
    backButton.addEventListener('click', function () {
        currentStep = currentStep - 1;
        console.log(currentStep);
        setActiveStep();
    })

    initForm();

})();

