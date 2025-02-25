let triesLeft = 5;
const random = Math.floor(Math.random() * 100) + 1;

function checknumber() {
    const guessInput = document.getElementById('guess'); 
    const guess = guessInput.value;
    const message = document.getElementById('message');
    const triesDisplay = document.getElementById("tries");

    if (triesLeft > 1) {
        triesLeft--;

        if (guess == random) {
            message.innerHTML = "Correct!";
            message.style.color = 'green';
        } else if (guess > random) {
            message.innerHTML = 'Too high! Try again.';
            message.style.color = 'red';
        } else if (guess < random) {
            message.innerHTML = 'Too low! Try again.';
            message.style.color = 'orange';
        }  

        triesDisplay.innerHTML = `Tries Left: ${triesLeft}`;
        guessInput.value = "";
    } else {
        message.innerHTML = `Game Over! The number was ${random}.`;
        message.style.color = 'red';
        triesDisplay.innerHTML = "0 tries left!";
        guessInput.disabled = true;
    }
}
