// console.log("hello Universe/.........");

const usernameField = document.querySelector("#usernameField")
const feedbackArea = document.querySelector(".invalid-feedback")
const emailField = document.querySelector("#emailField")
const emailfeedbackArea = document.querySelector(".invalid-mail")
const togglepwd = document.querySelector(".togglePWD")
const passwordField = document.querySelector("#passwordField")
const submitbtn = document.querySelector(".submit-btn")

togglepwd.addEventListener("click", (e) =>{
    if(togglepwd.textContent === "SHOW"){
        togglepwd.textContent = "HIDE"
        passwordField.setAttribute("type","text")
    }else {
        togglepwd.textContent = "SHOW"
        passwordField.setAttribute("type","password")
    }
})

usernameField.addEventListener("keyup",(e) =>{
    const username = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";

    if(username.length > 0){
        fetch('/authentication/validateUser',{
            body: JSON.stringify({username:username}),
            method : "POST"
        }).then((res) => res.json())
        .then((data) =>{
            if(data.username_error){
                submitbtn.setAttribute("disabled","disabled");
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
            }else{
                submitbtn.removeAttribute("disabled");
            }
        })
    }
})

emailField.addEventListener("keyup",(e)=>{
    const emailid = e.target.value;
    emailField.classList.remove("is-invalid");
    // emailfeedbackArea.style.display = "none";

    if(emailid.length > 0){
        fetch('/authentication/validateEmail',{
        body: JSON.stringify({email:emailid}),
        method: "POST"
    }).then((res)=>res.json())
    .then((data)=>{
            console.log(data)
            if(data.email_error){
                submitbtn.setAttribute("disabled", "disabled");
                emailField.classList.add("is-invalid");
                submitbtn.disabled = true;
                // emailfeedbackArea.style.display = "block";
                // emailfeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
            }else{
                submitbtn.removeAttribute("disabled");
            }
    })
    }
})
