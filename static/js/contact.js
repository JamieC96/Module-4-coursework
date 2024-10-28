const named = document.getElementById("named")
const number = document.getElementById("number")
const email = document.getElementById("email")
const form = document.getElementById("form")

const named_error = document.getElementById("named_error")
const email_error = document.getElementById("email_error")
const number_error = document.getElementById("number_error")

form.addEventListener("submit", (e) =>
{   var email_check = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/; 
    var number_check = /^\d{10}$/;


    if(named.value === "" || named.value == null)
{e.preventDefault();
    named_error.innerHTML = "Name is required";
}
    else 
    { 
        named_error.innerHTML = "";
    }


    if(!email.value.match(email_check))
{e.preventDefault();
    email_error.innerHTML = "Invalid Email";
}
else 
    { 
        email_error.innerHTML = "";
    }

    if(!number.value.match(number_check))
{e.preventDefault();
    number_error.innerHTML = "Invalid phone number, make sure the number is 10 digits long with no spaces";
}
else 
    { number_error.innerHTML = "";
    }
})
