const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

const username = document.getElementById('username');
const password = document.getElementById('password');
const loginSubmit = document.getElementById('login-submit');
const submitToChatgpt = document.querySelector('#submit-to-chatgpt');
const prompt = document.querySelector('#prompt');
const chatresponse = document.querySelector('#chat_response')

// const adminCredentials = {
//     username: 'admin',
//     password: 'password'
// }

// loginSubmit.addEventListener('click', (e) => {
//     e.preventDefault();
//     if(username.value === adminCredentials.username && password.value === adminCredentials.password) {
//         console.log('You are an admin');
//     }
// })

if(registerBtn){
  registerBtn.addEventListener('click', (e) => {
    container.classList.add('active');
  });
}

if(loginBtn){
  loginBtn.addEventListener('click', (e) => {
    container.classList.remove('active');
  });
}

if(submitToChatgpt){
  submitToChatgpt.addEventListener('click', async function(e){
    e.preventDefault()

    const response = await fetch("/homepage/chatbot/",{
      method:"POST",
      headers: {"Content-type":"application/json"},
      body: JSON.stringify({message: prompt.value}),
    })
    console.log(response)

    let reader = response.body.getReader();

    let output = "";

    while(true){
      const {done, value} = await reader.read();
      output += new TextDecoder().decode(value);
      chatresponse.innerHTML = marked.parse(output);

      if(done){
        console.log(marked.parse(output))
        return
      }
    }
  })
}
