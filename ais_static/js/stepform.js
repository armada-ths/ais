//Global Variables
let currentStep;
let numberSteps;
let nextButton;
let backButton;
let submitButton;
let formSteps;
let browser;
let companyTitle;
let list;
let writingtimer;
let stepTrackerChildren;
let requiredElementsForm;
let form;
let timeout;

function init() {
    //Get elements from DOM
    numberSteps = document.getElementsByClassName('form-step').length;
    formSteps = document.getElementsByClassName('form-step');
    nextButton = document.getElementById('next-step-btn');
    backButton = document.getElementById('back-step-btn');
    submitButton = document.getElementById('submit-form-btn');
    browser = document.getElementById('browser');
    companyTitle = document.getElementById('company-confirmation-title');
    list = document.getElementById('company-list');
    stepTrackerChildren = document.getElementById('form-step-tracker').children;
    form = document.getElementById('user-registration-form');

    //Setting static initial values
    currentStep = 0;
    browser.placeholder = 'Type your company name...';
    writingtimer = 500
    requiredElementsForm = [];
    timeout = null;

    //Remove class 'no-transition' from all trackers. 'no-transition' is a CSS class that prevents animations from happening. Elements in DOM are initialized with it 
    //to not execute animations when loading, which would effect at the aesthetics of the webpage. Once they are load, animations can now be played.
    for (let i = 0; i < stepTrackerChildren.length; i++) {
        stepTrackerChildren[i].classList.remove('no-transition');
    }

    //Creation of an array o arrays that contains all the 'required' form input tags of each step. Will be later used for validation purposes
    for (let i = 0; i < formSteps.length; i++) {
        let slice = [...Array.prototype.slice.call(formSteps[i].querySelectorAll("[required]"))];
        requiredElementsForm = [...requiredElementsForm, slice];
    }
}

//Colors the step in green if the user has reached it
function colorStepNumber() {
    for (let i = 0; i < stepTrackerChildren.length; i++) {
        //If the step is greater than the current step we turn it to active
        if (i > currentStep) {
            stepTrackerChildren[i].classList.remove('active');
        } else {
            stepTrackerChildren[i].classList.add('active');
        }
    }
}

//Makes the 'next', 'back' and 'submit' button visible (or not) depending on the actual step. It can also modify the content of 'next' and 'back button
function setVisibleButtons(next, back, submit, confirmation) {
    //Visibility
    ((next) ? nextButton.style.display = 'inline-block' : nextButton.style.display = 'none');
    ((back) ? backButton.style.display = 'inline-block' : backButton.style.display = 'none');
    ((submit) ? submitButton.style.display = 'inline-block' : submitButton.style.display = 'none');

    //Content. The boolean variable: 'confirmation' is used to determine the content of the 'next' and 'back button
    if (confirmation) {
        nextButton.innerHTML = 'Yes';
        backButton.innerHTML = 'No';
    } else {
        nextButton.innerHTML = 'Next';
        backButton.innerHTML = 'Back';
    }
}

//Sets the active form step depending on the number of clicks on the 'next' button
function setActiveStep() {
    //Changes classes from <div> tags in DOM to make the active step visible and the rest invisible
    for (let i = 0; i < numberSteps; i++) {
        ((currentStep == i) ? formSteps[i].setAttribute('id', 'activeStep') : formSteps[i].removeAttribute('id'));
    }

    //Calls the setVisibleButtons() with the specific configuration for that step
    if (currentStep == 0) {
        //Reset browser each time we go back to it
        browser.value = '';
        list.innerHTML = '';

        //Shows the browser and hides the 'company confirmation' page
        document.getElementById('company-confirmation').style.display = 'none';
        document.getElementById('company-search').style.display = 'block';
        setVisibleButtons(false, false, false, false);

    } else if (currentStep == numberSteps - 1) {
        setVisibleButtons(false, true, true, false);
    } else {
        setVisibleButtons(true, true, false, false);
    }

    //Color the steps to green to indicate the user in which step its currently in
    colorStepNumber();
}

function validateStep(stepNumber) {
    //Validates all required input tags in the current step
    for (let i = 0; i < requiredElementsForm[stepNumber].length; i++) {
        if (!requiredElementsForm[stepNumber][i].checkValidity()) {
            requiredElementsForm[stepNumber][i].reportValidity();
            return false;
        }
    }
    return true;
}

function validate(submit) {
    if (submit) {
        //This part is only executed before submitting the form. It basically validates all steps again.
        for (let i = 0; i < requiredElementsForm.length; i++) {

            if (!validateStep(i)) {
                currentStep = i;
                setActiveStep();
            }
        }
    } else {
        //This part is executed only when the form is loaded. The code looks for the DOM elements with the class 'form-control-danger'
        //which Django places in those form elements that were incorrect when the form was last submitted. If any of these elements
        //is found, then the form jumps to the right step, so that the user knows which step needs to be corrected.
        let requiredElementsFlat = requiredElementsForm.flat();
        for (let i = 0; i < requiredElementsFlat.length; i++) {
            if (requiredElementsFlat[i].classList.contains('form-control-danger')) {
                if (requiredElementsFlat[i].type == 'password')
                    currentStep = 2;
                else if (requiredElementsFlat[i].id == 'browser')
                    currentStep = 0;
                else
                    currentStep = 1;

                break;
            }
        }

    }
}

function initBrowser() {
    browser.addEventListener('keyup', function (e) {
        clearTimeout(timeout);
        // Make a new timeout set to go off in 1000ms (1 second)
        timeout = setTimeout(function () {

            //Remove all elements from list
            while (list.firstChild) {
                list.removeChild(list.lastChild);
            }

            //Makes list not visible when the input is empty
            if (browser.value.replace(/[` ~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, '').length == 0) {
                list.style.visibility = 'hidden'
            } else {
                //Fetches the top 10 companies related to the input search
                fetch("http://localhost:3000/api/companies?limit=10&input=" + browser.value).then((response) => response.json()).then((json) => {
                    //Create a list element for each company returned
                    for (var i = 0; i < json.length; i++) {
                        //Name of company
                        const newCompany = document.createElement("span");
                        newCompany.innerHTML = json[i]["Organization Name"];
                        newCompany.value = json[i]["id"];

                        //Div tag that encloses the name. The span is now appended to it
                        const div = document.createElement("div");
                        div.classList.add("p-2");
                        div.appendChild(newCompany);

                        //Link tag that encloses the div
                        const listElement = document.createElement("a");
                        listElement.appendChild(div);

                        //Append this new object to the list
                        list.appendChild(listElement);

                        //Add an event listener to it that triggers the confirmation and sets the selected value as the company
                        listElement.addEventListener('click', function () {
                            //Set selected value as the <input> value
                            companyTitle.innerHTML = newCompany.innerHTML;
                            browser.value = newCompany.value;

                            //Trigger confirmation
                            document.getElementById('company-confirmation').style.display = 'block';
                            document.getElementById('company-search').style.display = 'none';
                            setVisibleButtons(true, true, false, true);
                        });
                    }

                    //Makes list visible
                    list.style.visibility = 'visible'
                });
            }
        }, writingtimer);
    });
}

(function () {
    init();
    validate(false);
    setActiveStep();
    initBrowser();

    nextButton.addEventListener('click', function () {
        //Limiting the step amount between 0 and numberSteps
        if (currentStep < numberSteps - 1 && validateStep(currentStep)) {
            currentStep = currentStep + 1;
            setActiveStep();
        }
    });

    backButton.addEventListener('click', function () {
        if (currentStep > 0) {
            //Limiting the step amount between 0 and numberSteps
            currentStep = currentStep - 1;
        }
        setActiveStep();
    });

    submitButton.addEventListener('click', function () {
        //Validate all form
        validate(true);
        if (form.reportValidity()) {
            //Submit if client-side validation is correct
            form.submit();
        }
    });

})();