const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

const username = document.getElementById('username');
const password = document.getElementById('password');
const loginSubmit = document.getElementById('login-submit');
const adminCredentials = {
    username: 'admin',
    password: 'password'
}

loginSubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if(username.value === adminCredentials.username && password.value === adminCredentials.password) {
        console.log('You are an admin');
    }
})

registerBtn.addEventListener('click', (e) => {
  container.classList.add('active');
});

loginBtn.addEventListener('click', (e) => {
  container.classList.remove('active');
});
