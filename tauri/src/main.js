const { invoke } = window.__TAURI__.tauri;

async function syscall() {
  await invoke('syscall_test', {});
}
async function open_project() {
  await invoke('open_project', {});
  window.location.href = "index2.html";
}

window.addEventListener("DOMContentLoaded", () => {
  document
    .querySelector("#open-project")
    .addEventListener("click", () => open_project());
});
