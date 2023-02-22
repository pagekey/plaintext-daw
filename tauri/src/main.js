const { invoke } = window.__TAURI__.tauri;

let greetInputEl;
let greetMsgEl;

async function greet() {
  // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
  greetMsgEl.textContent = await invoke("greet", { name: greetInputEl.value });
}

async function syscall() {
  await invoke('syscall_test', {});
}
async function open_project() {
  await invoke('open_project', {});
}

window.addEventListener("DOMContentLoaded", () => {
  greetInputEl = document.querySelector("#greet-input");
  greetMsgEl = document.querySelector("#greet-msg");
  document
    .querySelector("#greet-button")
    .addEventListener("click", () => greet());
  document
    .querySelector("#syscall-button")
    .addEventListener("click", () => syscall());
  document
    .querySelector("#open-project")
    .addEventListener("click", () => open_project());
});
