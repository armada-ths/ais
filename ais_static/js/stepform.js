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

function init() {
    //Initialize step and max number of steps
    currentStep = 0;
    numberSteps = document.getElementsByClassName('form-step').length;

    //Find Buttons
    nextButton = document.getElementById('next-step-btn');
    backButton = document.getElementById('back-step-btn');
    submitButton = document.getElementById('submit-form-btn');

    formSteps = document.getElementsByClassName('form-step');
    browser = document.getElementById('browser');

    //This is the <p> in the second step (confirmation company step) which shows the company name. Will be used to display the company name selected from the browser
    companyTitle = document.getElementById('company-confirmation-title');

    //List of companies resulted from the browsing
    list = document.getElementById('company-list');

    browser.placeholder = 'Type your company name...';

    //Time that needs to pass after a user input for browser to initiate a search 
    writingtimer = 500
}

//Sets the active form step depending on the number of clicks on the 'next' button
function setActiveStep() {
    for (let i = 0; i < formSteps.length; i++) {
        if (currentStep == i) {
            formSteps[i].setAttribute('id', 'activeStep');
        } else {
            formSteps[i].removeAttribute('id');
        }
    }

    //Reset browser each time we go back to it
    if (currentStep == 0) {
        browser.value = '';
        list.innerHTML = '';
    }
}

//Makes the 'next', 'back' and 'submit' button visible (or not) depending on the actual step
function setVisibleButtons() {
    submitButton.style.display = 'none';
    if (currentStep == 0) {
        //When browser is visible, no buttons are shown
        nextButton.style.display = 'none';
        backButton.style.display = 'none';
        submitButton.style.display = 'none';
        browser.value = '';
    } else if (currentStep == numberSteps - 1) {
        //In last step, all buttons are shown except the 'next' button since there's no step after this one
        nextButton.style.display = 'none';
        submitButton.style.display = 'inline-block';
    } else {
        //Otherwise, all buttobns are shown except the 'submit' button, which is only shown at last step
        nextButton.style.display = 'inline-block';
        backButton.style.display = 'inline-block';
    }

    if (currentStep == 1) {
        nextButton.innerHTML = 'Yes';
        backButton.innerHTML = 'No';
    } else {
        nextButton.innerHTML = 'Next';
        backButton.innerHTML = 'Back';
    }
}

function initBrowser() {
    //Typing timer initialized to 1000ms
    let timeout = null;


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
                fetch("http://localhost:3000/api/companies?limit=10&input=" + browser.value).then((response) => response.json())
                    .then((json) => {

                        //Create a list element for each company returned
                        for (var i = 0; i < json.length; i++) {
                            const newCompany = document.createElement("span");
                            newCompany.innerHTML = json[i]["Organization Name"];

                            const div = document.createElement("div");
                            div.classList.add("p-2");
                            div.appendChild(newCompany);

                            const listElement = document.createElement("a");
                            listElement.appendChild(div);

                            list.appendChild(listElement);

                            listElement.addEventListener('click', function () {
                                companyTitle.innerHTML = newCompany.innerHTML;
                                browser.value = newCompany.innerHTML;
                                currentStep = currentStep + 1;
                                setActiveStep();
                                setVisibleButtons(currentStep);
                            })
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
    setActiveStep();
    setVisibleButtons();
    initBrowser();

    nextButton.addEventListener('click', function () {
        //Limiting the step amount between 0 and numberSteps
        if (currentStep < numberSteps - 1) {
            currentStep = currentStep + 1;
            setActiveStep();
            setVisibleButtons(currentStep, numberSteps);

        }
    })

    backButton.addEventListener('click', function () {
        if (currentStep == 2) {
            //Skip confirmation step when going back
            currentStep = 0;
            setActiveStep();
            setVisibleButtons(currentStep, numberSteps);
        } else if (currentStep > 0) {
            //Limiting the step amount between 0 and numberSteps
            currentStep = currentStep - 1;
            setActiveStep();
            setVisibleButtons(currentStep, numberSteps);
        }
    })
})();