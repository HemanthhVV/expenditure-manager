
const togglepwd = document.querySelector(".togglePWD")
const togglepwd2 = document.querySelector(".toggleConfirm")
const passwordField = document.querySelector("#passwordField")
const passwordField2 = document.querySelector("#confirmField")


togglepwd.addEventListener("click", (e) => {
    if (togglepwd.textContent === "SHOW") {
        togglepwd.textContent = "HIDE"
        passwordField.setAttribute("type", "text")
    } else {
        togglepwd.textContent = "SHOW"
        passwordField.setAttribute("type", "password")
    }
})

togglepwd2.addEventListener("click", (e) => {
    if (togglepwd2.textContent === "SHOW") {
        togglepwd2.textContent = "HIDE"
        passwordField2.setAttribute("type", "text")
    } else {
        togglepwd2.textContent = "SHOW"
        passwordField2.setAttribute("type", "password")
    }
})

