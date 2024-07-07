const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");

let users = []; // Array to store users

// Add event listener to sign up button to add class
signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

// Add event listener to sign in button to remove class
signInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

function registerUser() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("signUpPass").value;

  if (name && email && password) {
    const user = {
      name: name,
      email: email,
      password: password
    };

    users.push(user);
    alert("User registered successfully!");
    document.getElementById("signUpForm").reset();
    container.classList.remove("right-panel-active"); // Switch to sign in panel
  } else {
    alert("Please fill all fields.");
  }
}

function check() {
  const user = document.getElementById("user").value;
  const pass = document.getElementById("pass").value;
  
  const loggedInUser = users.find(u => u.email === user && u.password === pass);
  
  if (loggedInUser) {
    window.location.href = "index.html";
  } else {
    window.alert("Invalid username or password");
  }
}
console.log(user);