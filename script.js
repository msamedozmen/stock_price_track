function handleTextInput(value) {
    const submitButton = document.querySelector(".stForm > .submit-button");
    if (value.trim() === "") {
        submitButton.setAttribute("disabled", "true");
    } else {
        submitButton.removeAttribute("disabled");
    }
}

const textInput = document.querySelector("input[data-baseweb='input']");
textInput.addEventListener("input", function(event) {
    handleTextInput(event.target.value);
});

handleTextInput(textInput.value);


