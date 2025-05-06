const container = document.querySelector(".container");
const registerBtn = document.querySelector(".register-btn");
const loginBtn = document.querySelector(".login-btn");

const username = document.getElementById("username");
const password = document.getElementById("password");
const loginSubmit = document.getElementById("login-submit");
const submitToChatgpt = document.querySelector("#submit-to-chatgpt");
const generateEpisodes = document.querySelector("#generate-episodes");
const generateFacilitatorScript = document.querySelector(
  "#generate-facilitator-script"
);
const generateContent = document.querySelector("#generate-content");
const prompt = document.querySelector("#prompt");
const chatresponse = document.querySelector("#chat_response");
const generatePptx = document.querySelector("#generate-pptx");
const downloadPptx = document.querySelector("#download-pptx");
const message = document.querySelector("#message");
let fileName = "";
let lessonPlanSaveState = ""
let episodesSaveState = ""
let contentSaveState = ""
let facilitatorScriptSaveState = ""

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

//Revise this, change the parameter into string instead of array
function format_chatgpt_response(paragraph) {
  const headingOrBold = /^(###)|^\*\*.*\*\*$/;
  const hrAndDash = /^(<hr>|---)$/;

  /**
   * Headings = Starts with ### and ends with \n
   */
  let sentences = paragraph.split("\n");
  //console.log(sentences)

  for (let i = 0; i < sentences.length; i++) {
    console.log(sentences[i])
    let trimmed_sentence = sentences[i].replace(/[#*]/g,"");
    let trimmed_whitespace = sentences[i].trim()
    if (trimmed_whitespace.match(headingOrBold)) {
      sentences[i] = sentences[i].replace(sentences[i], `<h3>${trimmed_sentence}</h3>`);
    } else if (sentences[i] == "" && sentences[i+1]) {
      sentences[i] = sentences[i].replace(sentences[i], `<hr>`);
    } else if (sentences[i].match(hrAndDash)) {
      sentences[i] = sentences[i].replace(sentences[i], `<hr>`);
    } else if(sentences[i] == ""){
      continue;
    } else {
      sentences[i] = sentences[i].replace(sentences[i], `<p>${trimmed_sentence}</p>`);
    }
  }
  return sentences.join("\n");
}

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
    fileName = "lesson_plan.pptx";
    if (chatresponse.innerHTML != " ") {
      console.log("ivan too");
      generatePptx.style.display = "block";
      generateEpisodes.style.display = "block";
      //generateContent.style.display = "block";
      //generateFacilitatorScript.style.display = "block";
    }
    if (generateContent.checkVisibility()) {
      generateContent.style.display = "none";
    }
    if (generateFacilitatorScript.checkVisibility()) {
      generateFacilitatorScript.style.display = "none";
    }
    const response = await fetch("/homepage/chatbot/", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ message: prompt.value }),
    });
    console.log(response);

    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      //console.log(output)
      //chatresponse.innerHTML = marked.parse(output);

      if (done) {
        //let splitted = output.split("\n")
        lessonPlanSaveState = output
        console.log(output)
        chatresponse.innerHTML = format_chatgpt_response(output);
        //console.log(format_chatgpt_response(output));
        //console.log(output)
        //console.log(marked.parse(output));
        return;
      }
    }
  });
}

if (generateEpisodes) {
  generateEpisodes.addEventListener("click", async (e) => {
    e.preventDefault();
    //submitToChatgpt.style.display = "none";
    generateContent.style.display = "block";
    fileName = "episodes.pptx";
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector(
      "input[name=csrfmiddlewaretoken]"
    ).value;
    const response = await fetch("/homepage/generate_episodes/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json",
      },
      //body: JSON.stringify({ message: chatresponse.textContent }),
      body: JSON.stringify({ message: lessonPlanSaveState }),
    });
    console.log(chatresponse.textContent);
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      //chatresponse.innerHTML = marked.parse(output);

      if (done) {
        episodesSaveState = output
        console.log(output);
        chatresponse.innerHTML = format_chatgpt_response(output);
        return;
      }
    }
  });
}

if (generateContent) {
  generateContent.addEventListener("click", async (e) => {
    e.preventDefault();
    //generateEpisodes.style.display = "none";
    generateFacilitatorScript.style.display = "block";
    fileName = "content.pptx";
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector(
      "input[name=csrfmiddlewaretoken]"
    ).value;
    const response = await fetch("/homepage/generate_content/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json",
      },
      //body: JSON.stringify({ message: chatresponse.textContent }),
      body: JSON.stringify({ message: episodesSaveState }),
    });
    //console.log(response)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      //chatresponse.innerHTML = marked.parse(output);

      if (done) {
        contentSaveState = output
        console.log(output);
        chatresponse.innerHTML = format_chatgpt_response(output);
        return;
      }
    }
  });
}

if (generateFacilitatorScript) {
  generateFacilitatorScript.addEventListener("click", async (e) => {
    e.preventDefault();
    //generateContent.style.display = "none";
    fileName = "facilitator_script.pptx";
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector(
      "input[name=csrfmiddlewaretoken]"
    ).value;
    const response = await fetch("/homepage/generate_facilitator_script/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json",
      },
      //body: JSON.stringify({ message: chatresponse.textContent }),
      body: JSON.stringify({ message: contentSaveState }),
    });
    //console.log(response)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      //chatresponse.innerHTML = marked.parse(output);

      if (done) {
        facilitatorScriptSaveState = output
        console.log(output);
        chatresponse.innerHTML = format_chatgpt_response(output);
        return;
      }
    }
  });
}

if (generatePptx) {
  generatePptx.addEventListener("click", async (e) => {
    e.preventDefault();
    //console.log(chatresponse.textContent)
    let csrf_token = document.querySelector(
      "input[name=csrfmiddlewaretoken]"
    ).value;
    await fetch("/homepage/generate_pptx/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        message: chatresponse.innerHTML,
        filename: fileName,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        //downloadPptx.style.display = "block";
        downloadPptx.disabled = false;
        downloadPptx.setAttribute("filename", data.filename);
        //message.style.display = "block"
        message.textContent = `${data.message}`;
        setTimeout(() => {
          //message.style.display = "none"
          message.textContent = "";
        }, 3000);
      });
  });
}

if (downloadPptx) {
  downloadPptx.addEventListener("click", (e) => {
    e.preventDefault();
    let fileNameAttribute = downloadPptx.getAttribute("filename");
    const url = `/homepage/download/${fileNameAttribute}`;
    const a = document.createElement("a");
    a.href = url;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    downloadPptx.removeAttribute("filename");
    //downloadPptx.style.display = "none"
    downloadPptx.disabled = true;
  });
}
