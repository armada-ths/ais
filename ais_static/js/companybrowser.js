(function () {
    let browser = document.getElementById('browser');
    let timeout = null;
    let writingtimer = 1000
    browser.addEventListener('keyup', function (e) {
        clearTimeout(timeout);
        // Make a new timeout set to go off in 1000ms (1 second)
        timeout = setTimeout(function () {
            console.log('Input Value:', browser.value);
            fetch("0.0.0.0:3000/api/companies").then((response) => response.json())
                .then((json) => console.log(json));
        }, writingtimer);


    });
}
)();