//Global Variables
let currentStep;
let numberSteps;
let nextButton;
let backButton;
let submitButton;
let registerCompanyButton;
let formSteps;
let browser;
let companyTitle;
let list;
let writingtimer;
let stepTrackerChildren;
let requiredElementsForm;
let requiredElementsRegisterCompanyForm;
let form;
let companyRegistrationForm;
let companyRegistrationInputs;
let timeout;
let noResults;
let collapsibleButtons;
let companyRegistration;

function init() {
    //Get elements from DOM
    numberSteps = document.getElementsByClassName('form-step').length;
    formSteps = document.getElementsByClassName('form-step');
    nextButton = document.getElementById('next-step-btn');
    backButton = document.getElementById('back-step-btn');
    submitButton = document.getElementById('submit-form-btn');
    registerCompanyButton = document.getElementById('register-company-btn');
    browser = document.getElementById('browser');
    companyTitle = document.getElementById('company-confirmation-title');
    list = document.getElementById('company-list');
    stepTrackerChildren = document.getElementById('form-step-tracker').children;
    form = document.getElementById('user-registration-form');
    companyRegistrationForm = document.getElementById('company-regitration-form');
    companyRegistrationInputs = document.getElementById('company-registration-inputs');
    noResults = document.getElementById('company-list-no-results');
    collapsibleButtons = document.getElementsByClassName('collapsible-preview');

    //Setting static initial values
    currentStep = 0;
    browser.placeholder = 'Type your company name...';
    writingtimer = 500
    requiredElementsForm = [];
    requiredElementsRegisterCompanyForm = [];
    timeout = null;
    companyRegistration = false; //If false (default), the script will send the user registration form with an existing company form. Otherwise, if true, willregister a new company and the user under that company

    //Remove class 'no-transition' from all trackers. 'no-transition' is a CSS class that prevents animations from happening. Elements in DOM are initialized with it 
    //to not execute animations when loading, which would effect at the aesthetics of the webpage. Once they are load, animations can now be played.
    for (let i = 0; i < stepTrackerChildren.length; i++) {
        stepTrackerChildren[i].classList.remove('no-transition');
    }

    //Creation of an array o arrays that contains all the 'required' form input tags of each step. Will be later used for validation purposes
    let slice = [];
    for (let i = 0; i < formSteps.length; i++) {
        //Distribute these elements in:
        // - requiredElementsForm => list of required elements of the form in case the company is already registered (company found using browser)
        // - requiredElementsRegisterCompanyForm => list of required elements of the form in case the company is not registered (currently ALL except the input with id = 'browser)
        slice = [...Array.prototype.slice.call(formSteps[i].querySelectorAll("[required]"))];

        requiredElementsForm = [...requiredElementsForm, slice.filter(element => !companyRegistrationForm.contains(element))];
        requiredElementsRegisterCompanyForm = [...requiredElementsRegisterCompanyForm, slice.filter(element => element.id != 'browser')];
    }

    //Add an event listener to all collapsibles. This is so collapse or show the content depending on the content current height
    for (let i = 0; i < collapsibleButtons.length; i++) {
        collapsibleButtons[i].addEventListener('click', function (event) {
            //If the height is greater than 0, we collapse the content. Otherwise we show it
            let content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                event.target.classList.remove("active");
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                event.target.classList.add("active");
            }
        });
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
        companyRegistrationForm.style.display = 'block';
        setVisibleButtons(false, false, false, false);

    } else if (currentStep == numberSteps - 1) {
        setVisibleButtons(false, true, true, false);
    } else {
        setVisibleButtons(true, true, false, false);
    }

    //Erase company information depending on case scenario when jumping from step 0 to step 1 in order to avoid the form submitting both
    //types of information (since one path excludes the other)
    eraseCompanyInformation();
    //Color the steps to green to indicate the user in which step its currently in
    colorStepNumber();
}

function eraseCompanyInformation() {
    //If the user submits a company name, all the inputed value inside the collapsible is erased. Otherwise, if the user clicks on the 'register company' button, 
    //the company name provided is erased. This is done in order to minimize user errors
    if (companyRegistration) {
        browser.value = "";
    } else {
        [...companyRegistrationInputs.querySelectorAll("input")].forEach(element => {
            element.value = "";
        });
    }
}

function validateStep(stepNumber, requiredElementsForm, jumpStep) {
    //Validates all required input tags in the current step
    for (let i = 0; i < requiredElementsForm[stepNumber].length; i++) {
        if (!requiredElementsForm[stepNumber][i].checkValidity()) {
            //For some reason, some times the function reportValidity() does not display the error correctly if the function is called before the input is visible
            //This code allows the webpage to first jump into the step containing the error and the show the error in order for the error message to be displayed correctly
            //This code is of course optional and entirely dependant on the passed variable 'jumpStep'
            if (jumpStep) {
                currentStep = stepNumber;
                setActiveStep();
            }
            requiredElementsForm[stepNumber][i].reportValidity();
            return false;
        }
    }
    return true;
}

function validate(submit) {
    if (submit) {
        //The required elements from the registration process  are checked depending on the companyRegistration variable value which determines the path taken (registration with existent company or regitstration of user and company)
        let nonRequired = null;
        //Determining the required elements and the validation function depending on the path taken. Some elements might be required (or not) depending on the selected path, therefore its validation also varies depending on it
        if (companyRegistration) {
            //In this case, aside from the user info. and the password, the extra data that needs to be validated is the one inside the collapsible 
            requiredElements = requiredElementsRegisterCompanyForm;
            nonRequired = requiredElementsForm;
        } else {
            //In this case, aside from the user info. and the password, the only extra required data is the company that the user will be registered to
            requiredElements = requiredElementsForm;
            nonRequired = requiredElementsRegisterCompanyForm;
        }

        let successful = true;
        for (let i = 0; i < requiredElements.length; i++) {
            if (!validateStep(i, requiredElements, true)) {
                successful = false;
            }
        }

        //Set all required elements from the other path to non required in order for the browser to not report them. This will be later processed in the server to avoid errors
        if (successful) {
            notRequiredElements = nonRequired.flat().filter(x => !requiredElements.flat().includes(x));
            notRequiredElements.flat().forEach(element => element.required = false);
            form.submit();
        }
    } else {
        //This part is executed only when the form is loaded. The code looks for the DOM elements with the class 'form-control-danger'
        //which Django places in those form elements that were incorrect when the form was last submitted. If any of these elements
        //is found, then the form jumps to the right step, so that the user knows which step needs to be corrected.
        let formInputElements = form.querySelectorAll('input');
        for (let i = 0; i < formInputElements.length; i++) {
            if (formInputElements[i].classList.contains('form-control-danger')) {
                //Go to the step were the error is displayed. This is selected depending on the id of the element.
                if (formInputElements[i].id.includes('password'))
                    currentStep = 2;
                else if (formInputElements[i].id.includes('id_contact'))
                    currentStep = 1;
                else {
                    currentStep = 0;
                    //If there's an error inside the collapsible, then we initiallize it open, so its not collapsed by setting the maxHeight to the viewport height
                    if (formInputElements[i].id != 'browser') {
                        formInputElements[i].closest(".collapsible-content").style.maxHeight = "100vh";
                        companyRegistrationForm.classList.add("active");
                    }
                }

                break;
            }
        }

    }
}

function initBrowser() {
    browser.addEventListener('keyup', function (e) {
        clearTimeout(timeout);

        //No Results Found text turns invisible each time a key is entered
        noResults.style.visibility = 'hidden';

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
                fetch("/api/companies?limit=10&input=" + browser.value).then((response) => response.json()).then((json) => {

                    //No Results Found text turns visible if no company is returned by API
                    if (json.length == 0)
                        noResults.style.visibility = 'visible';

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
                            companyRegistrationForm.style.display = 'none';
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

function execute() {
    init();
    validate(false);
    setActiveStep();
    initBrowser();

    nextButton.addEventListener('click', function () {
        //Limiting the step amount between 0 and numberSteps. Validate the step before jumping to the new one
        if (currentStep < numberSteps - 1 && validateStep(currentStep, requiredElementsForm, false)) {
            currentStep = currentStep + 1;
            setActiveStep();
        }
    });

    backButton.addEventListener('click', function () {
        if (currentStep > 0) {
            //Limiting the step amount between 0 and numberSteps
            currentStep = currentStep - 1;

            //Reset companyRegistration to false, since the user went back to the initial step
            if (currentStep == 0)
                companyRegistration = false;

        }
        setActiveStep();
    });

    submitButton.addEventListener('click', function () {
        //Validate all form
        validate(true);
    });

    registerCompanyButton.addEventListener('click', function () {
        //Validate all form
        if (validateStep(currentStep, requiredElementsRegisterCompanyForm, false)) {
            currentStep = currentStep + 1;
            //Set the path to 'register user + company'
            companyRegistration = true;
            setActiveStep();
        }
    });
}

(function () {
    if (document.readyState !== 'loading') {
        //document is already ready and JS can be executed
        execute();
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            //document was not ready and JS needs to wait for DOm to be fully loaded to be executed
            execute();
        });
    }
})();