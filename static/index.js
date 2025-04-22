const container = document.querySelector(".container");
const registerBtn = document.querySelector(".register-btn");
const loginBtn = document.querySelector(".login-btn");

const username = document.getElementById("username");
const password = document.getElementById("password");
const loginSubmit = document.getElementById("login-submit");
const submitToChatgpt = document.querySelector("#submit-to-chatgpt");
const generateEpisodes = document.querySelector("#generate-episodes");
const generateFacilitatorScript = document.querySelector("#generate-facilitator-script");
const generateContent = document.querySelector("#generate-content");
const prompt = document.querySelector("#prompt");
const chatresponse = document.querySelector("#chat_response");
const generatePptx = document.querySelector("#generate-pptx");
const downloadPptx = document.querySelector('#download-pptx');

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

if (registerBtn) {
  registerBtn.addEventListener("click", (e) => {
    container.classList.add("active");
  });
}

if (loginBtn) {
  loginBtn.addEventListener("click", (e) => {
    container.classList.remove("active");
  });
}

if (submitToChatgpt) {
  submitToChatgpt.addEventListener("click", async function (e) {
    e.preventDefault();
    if (chatresponse.innerHTML != "") {
      generatePptx.style.display = "block";
      generateEpisodes.style.display = "block";
      generateContent.style.display = "block";
      generateFacilitatorScript.style.display = "block";
    }
    const response = await fetch("/homepage/chatbot/", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ message: prompt.value }),
    });
    //console.log(response);

    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      chatresponse.innerHTML = marked.parse(output);

      if (done) {
        console.log(marked.parse(output));
        return;
      }
    }
  });
}


if(generateEpisodes){
  generateEpisodes.addEventListener("click", async(e) => {
    e.preventDefault();
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value
    const response =await fetch("/homepage/generate_episodes/", {
      method: "POST",
      headers: { 
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json" },
      body: JSON.stringify({ message: chatresponse.textContent }),
    })
    console.log(chatresponse.textContent)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      chatresponse.innerHTML = marked.parse(output);

      if (done) {
        console.log(marked.parse(output));
        return;
      }
    }
  })
}

if(generateContent){
  generateContent.addEventListener("click", async(e) => {
    e.preventDefault();
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value
    const response =await fetch("/homepage/generate_content/", {
      method: "POST",
      headers: { 
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json" },
      body: JSON.stringify({ message: chatresponse.textContent }),
    })
    //console.log(response)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      chatresponse.innerHTML = marked.parse(output);

      if (done) {
        console.log(marked.parse(output));
        return;
      }
    }
  })
}

if(generateFacilitatorScript){
  generateFacilitatorScript.addEventListener("click", async(e) => {
    e.preventDefault();
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value
    const response =await fetch("/homepage/generate_facilitator_script/", {
      method: "POST",
      headers: { 
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json" },
      body: JSON.stringify({ message: chatresponse.textContent }),
    })
    //console.log(response)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      chatresponse.innerHTML = marked.parse(output);

      if (done) {
        console.log(marked.parse(output));
        return;
      }
    }
  })
}

if(generatePptx){
  generatePptx.addEventListener("click", async(e) => {
    e.preventDefault();
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value
    const response =await fetch("/homepage/generate_pptx/", {
      method: "POST",
      headers: { 
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json" },
      body: JSON.stringify({ message: chatresponse.innerHTML }),
    })
    console.log(response)
  })
}

if(downloadPptx){
  downloadPptx.addEventListener("click", (e)=>{
    e.preventDefault()
    const url = '/homepage/download/'
    const a = document.createElement('a');
    a.href = url;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  })
}

