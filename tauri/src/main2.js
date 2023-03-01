const { invoke } = window.__TAURI__.tauri;


window.addEventListener("DOMContentLoaded", async () => {
    console.log('calling get_filepath');
    invoke('get_filepath').then((fpath) => {
        document
            .querySelector("#current_project").innerHTML = fpath;
    });
});
