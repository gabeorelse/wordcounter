class Login {
    constructor(username, password) {
        this.username = username
        this.password = password
    }

    async validateCreds() {
        const data = JSON.stringify ({
            username: this.username,
            plain_password: this.password
        });
        const options = {
            method: 'POST',
            credentials: 'include',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
              },
            body: data
        };
        try {
            console.log('Fetch request starting...');
            const response = await fetch('http://localhost:5000/login', options);
            if (!response.ok) {
                const err = await response.json();
                console.log("Is this working?");
                throw new Error (err.error);
            }
            const data = await response.json();
            if (data.success) {
                window.location.href = '/user_home';
            } 
        } catch (error) {
            console.error('Error:', error.message);
            if (error.message.includes("No user exists")) {
                console.log("The error message includes this.")
                document.getElementById("error").innerHTML = "No user exists with these credentials.";
            } else {
                document.getElementById("error").innerHTML = "Login failed for reasons unknown. Please try again!";
            }
        }

    }

}

class Register {
    constructor (email, username, password) {
        this.email = email
        this.username = username
        this.password = password
    }

    async fetchData()  {
        const data = JSON.stringify ({
            email: this.email,
            username: this.username,
            plain_password: this.password
        });
        const options = {
            method: 'POST',
            credentials: 'include',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
              },
            body: data
        };
        try {
            const response = await fetch('http://localhost:5000/register', options);
            if (!response.ok) {
                const err = await response.json();
                throw new Error (err.error);
            }
            const data = await response.json();
            if (data.success) {
                window.location.href = '/login';
            }
            else {
                alert('Registration failed: ' + data.error);
                }
        } catch (error) {
            console.error('Error:', error.message);
            if (error.message == "Email already associated with an account.") {
                let login = document.getElementById("login");
                document.getElementById("error").innerHTML = "Email already associated with an account.";
                login.style.visibility = "visible";
            }
        }         
    }

}
        

const usernameInput = document.querySelector('input[name="username"]');
const passwordInput = document.querySelector('input[name="plain_password"]');

if (document.getElementById('submit')) {
    document.getElementById('submit').addEventListener('click', (event) => {
        if (!usernameInput.value || !passwordInput.value) {
            document.getElementById("error").innerHTML = "Cannot login without credentials!";
        } else {
            event.preventDefault();
            const loginInstance = new Login(usernameInput.value, passwordInput.value);
        
            loginInstance.validateCreds();
        }
    });
    
}

const emailInput = document.querySelector('input[name="email"]');
const userInput = document.querySelector('input[name="user"]');
const passInput = document.querySelector('input[name="password"]');

if (document.getElementById('register')) {
    document.getElementById('register').addEventListener('click', (event) => {
        if (!emailInput.value || !userInput.value || !passInput.value) {
            document.getElementById("error").innerHTML = "Cannot register user without credentials!";
        }
        else {
            event.preventDefault();
            console.log('Register button clicked');
            const registerInstance = new Register(emailInput.value, userInput.value, passInput.value);
    
            registerInstance.fetchData();
        }
    });
}

