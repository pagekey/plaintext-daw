const { invoke } = window.__TAURI__.tauri;


window.addEventListener("DOMContentLoaded", async () => {
    invoke('get_app').then((app) => {
        document
            .querySelector("#current_project").innerHTML = `filepath: ${app.filepath}\n\n\ncontents:: ${app.contents}`;
    });
});
