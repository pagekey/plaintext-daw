const { invoke } = window.__TAURI__.tauri;


window.addEventListener("DOMContentLoaded", async () => {
    invoke('get_app').then((app) => {
        document.querySelector("#filepath-value").innerHTML = app.filepath;
        document.querySelector("#bpm-value").innerHTML = app.song.bpm;
        document.querySelector("#sample-rate-value").innerHTML = app.song.sample_rate;
        document
            .querySelector("#current_project").innerHTML = `filepath: ${app.filepath}\n\n\ncontents:: ${app.contents}`;
    });
});
