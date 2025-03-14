const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

console.log(registerBtn);

registerBtn.addEventListener('click', (e) => {
  container.classList.add('active');
});

loginBtn.addEventListener('click', (e) => {
  container.classList.remove('active');
});
