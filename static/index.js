const container = document.querySelector(".container");
const registerBtn = document.querySelector(".register-btn");
const loginBtn = document.querySelector(".login-btn");

const username = document.getElementById("username");
const password = document.getElementById("password");
const loginSubmit = document.getElementById("login-submit");
const submitToChatgpt = document.querySelector("#submit-to-chatgpt");
//const generateEpisodes = document.querySelector("#generate-episodes");
const generateFacilitatorScript = document.querySelector(
  "#generate-facilitator-script"
);
const generateContent = document.querySelector("#generate-content");
const prompt = document.querySelector("#prompt");
const img = document.querySelector("#img");
//const chatresponse = document.querySelector("#chat_response");
const lessonResponse = document.querySelector("#lesson_plan");
//const episodeResponse = document.querySelector("#episodes");
const contentResponse = document.querySelector("#content");
const facilitatorScriptResponse = document.querySelector("#facilitator_script");
const generatePptx = document.querySelector("#generate-pptx");
//const downloadPptx = document.querySelector("#download-pptx");
const message = document.querySelector("#message");
let fileName = "lesson_plan.pptx";
let activeTab = document.querySelector("#lesson_plan");

const tabs = document.querySelectorAll(".tabs-heading li");
const contents = document.querySelectorAll(".tabs-body div");

if (tabs) {
  tabs.forEach((tab) => {
    tab.addEventListener("click", (e) => {
      const targetId = tab.getAttribute("data-target");

      //Change tab colors
      tabs.forEach((tab) => {
        tab.classList.remove("active");
      });
      tab.classList.add("active");

      contents.forEach((content) => {
        if (content.id == targetId && content.textContent != "") {
          console.log("active tab found and has content");
          fileName = `${content.id}.pptx`;
          activeTab = content;
          generatePptx.disabled = false;
        } else if (content.id == targetId && content.textContent == "") {
          console.log("active tab has no content");
          fileName = `${content.id}.pptx`;
          activeTab = content;
          generatePptx.disabled = true;
        }
        content.hidden = content.id !== targetId;
      });
    });
  });
}

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
    console.log(sentences[i]);
    let trimmed_sentence = sentences[i].replace(/[#*]/g, "");
    let trimmed_whitespace = sentences[i].trim();
    if (trimmed_whitespace.match(headingOrBold)) {
      sentences[i] = sentences[i].replace(
        sentences[i],
        `<h3>${trimmed_sentence}</h3>`
      );
    } else if (sentences[i] == "" && sentences[i + 1]) {
      sentences[i] = sentences[i].replace(sentences[i], `<hr>`);
    } else if (sentences[i].match(hrAndDash)) {
      sentences[i] = sentences[i].replace(sentences[i], `<hr>`);
    } else if (sentences[i] == "") {
      continue;
    } else {
      sentences[i] = sentences[i].replace(
        sentences[i],
        `<p>${trimmed_sentence}</p>`
      );
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
    message.textContent = "Generating please wait...";
    //fileName = "lesson_plan.pptx";
    if (lessonResponse.innerHTML != " ") {
      console.log("ivan too");
      //generatePptx.style.display = "block";
      //generateEpisodes.style.display = "block";
      generateContent.style.display = "block";
      //generateFacilitatorScript.style.display = "block";
    }
    // if (generateContent.checkVisibility()) {
    //   generateContent.style.display = "none";
    // }
    // if (generateFacilitatorScript.checkVisibility()) {
    //   generateFacilitatorScript.style.display = "none";
    // }
    const formData = new FormData();
    formData.append("message", prompt.value);

    // Append multiple files
    for (let i = 0; i < img.files.length; i++) {
      formData.append("images", img.files[i]);
    }
    const response = await fetch("/homepage/chatbot/", {
      method: "POST",
      body: formData,
      //body: JSON.stringify({ message: prompt.value, img: img.files }),
    });
    console.log(response);

    let reader = response.body.getReader();

    let output = "";

    const turndownService = new TurndownService();
    turndownService.addRule("horizontalRule", {
      filter: "hr",
      replacement: function () {
        return "\n\n---\n\n";
      },
    });

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      message.textContent = "Generating please wait...";
      //console.log(output)
      lessonResponse.innerHTML = marked.parse(output);

      if (done) {
        //lessonPlanSaveState = output;
        generatePptx.disabled = false;
        console.log(output);
        // lessonResponse.innerHTML = turndownService.turndown(
        //   lessonResponse.innerHTML
        // );
        //lessonResponse.innerHTML = marked.parse(output);
        lessonResponse.innerHTML = format_chatgpt_response(output);
        setTimeout(() => {
          //message.style.display = "none"
          message.textContent = "";
        }, 3000);
        return;
      }
    }
  });
}

// if (generateEpisodes) {
//   generateEpisodes.addEventListener("click", async (e) => {
//     e.preventDefault();
//     //submitToChatgpt.style.display = "none";
//     generateContent.style.display = "block";
//     //fileName = "episodes.pptx";
//     //console.log(chatresponse.textContent)
//     let csrf_token = document.querySelector(
//       "input[name=csrfmiddlewaretoken]"
//     ).value;
//     const response = await fetch("/homepage/generate_episodes/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrf_token,
//         "Content-type": "application/json",
//       },
//       //body: JSON.stringify({ message: chatresponse.textContent }),
//       body: JSON.stringify({ message: lessonResponse.textContent }),
//     });
//     console.log(episodeResponse.textContent);
//     let reader = response.body.getReader();

//     let output = "";

//     while (true) {
//       const { done, value } = await reader.read();
//       output += new TextDecoder().decode(value);
//       message.textContent = "Generating please wait...";
//       //chatresponse.innerHTML = marked.parse(output);

//       if (done) {
//         //episodesSaveState = output;
//         generatePptx.disabled = false;
//         console.log(output);
//         episodeResponse.innerHTML = format_chatgpt_response(output);
//         setTimeout(() => {
//           //message.style.display = "none"
//           message.textContent = "";
//         }, 3000);
//         return;
//       }
//     }
//   });
// }

if (generateContent) {
  generateContent.addEventListener("click", async (e) => {
    e.preventDefault();
    message.textContent = "Generating please wait...";
    //generateEpisodes.style.display = "none";
    generateFacilitatorScript.style.display = "block";
    //fileName = "content.pptx";
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
      body: JSON.stringify({ message: lessonResponse.textContent }),
    });
    //console.log(response)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      message.textContent = "Generating please wait...";
      contentResponse.innerHTML = marked.parse(output);

      if (done) {
        //contentSaveState = output;
        generatePptx.disabled = false;
        console.log(output);
        //contentResponse.innerHTML = marked.parse(output);
        contentResponse.innerHTML = format_chatgpt_response(output);
        setTimeout(() => {
          //message.style.display = "none"
          message.textContent = "";
        }, 3000);
        return;
      }
    }
  });
}

if (generateFacilitatorScript) {
  generateFacilitatorScript.addEventListener("click", async (e) => {
    e.preventDefault();
    //generateContent.style.display = "none";
    //fileName = "facilitator_script.pptx";
    //console.log(chatresponse.textContent)

    message.textContent = "Generating please wait...";
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
      body: JSON.stringify({ message: contentResponse.textContent }),
    });
    //console.log(response)
    let reader = response.body.getReader();

    let output = "";

    while (true) {
      const { done, value } = await reader.read();
      output += new TextDecoder().decode(value);
      facilitatorScriptResponse.innerHTML = marked.parse(output);

      if (done) {
        //facilitatorScriptSaveState = output;
        generatePptx.disabled = false;
        console.log(output);
        //facilitatorScriptResponse.innerHTML = marked.parse(output);
        facilitatorScriptResponse.innerHTML = format_chatgpt_response(output);
        setTimeout(() => {
          //message.style.display = "none"
          message.textContent = "";
        }, 3000);
        return;
      }
    }
  });
}

if (generatePptx) {
  generatePptx.addEventListener("click", async (e) => {
    e.preventDefault();
    let csrf_token = document.querySelector(
      "input[name=csrfmiddlewaretoken]"
    ).value;
    message.textContent = "Generating please wait...";
    const turndownService = new TurndownService();
    turndownService.addRule("horizontalRule", {
      filter: "hr",
      replacement: function () {
        return "\n\n---\n\n";
      },
    });
    turndownService.addRule("blockImage", {
      filter: "img",
      replacement: function (content, node) {
        const alt = node.alt || "";
        const src = node.getAttribute("src") || "";
        return `\n\n![${alt}](${src})\n\n`;
      },
    });
    const response = await fetch("/homepage/generate_pptx/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrf_token,
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        message: activeTab.innerHTML,
        //message: turndownService.turndown(activeTab.innerHTML),
        filename: fileName,
      }),
    });
    console.log(response);

    if (response.ok) {
      const blob = await response.blob();
      message.textContent = "";
      const downloadUrl = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = downloadUrl;
      a.download = fileName || "presentation.pptx"; // fallback name
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(downloadUrl);
    } else {
      const errorData = await response.json();
      console.error("Error generating PPTX:", errorData.error);
      alert("Failed to generate PowerPoint: " + errorData.error);
    }
  });
}

// if (downloadPptx) {
//   downloadPptx.addEventListener("click", (e) => {
//     e.preventDefault();
//     let fileNameAttribute = downloadPptx.getAttribute("filename");
//     const url = `/homepage/download/${fileNameAttribute}`;
//     const a = document.createElement("a");
//     a.href = url;
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     downloadPptx.removeAttribute("filename");
//     //downloadPptx.style.display = "none"
//     downloadPptx.disabled = true;
//   });
// }
