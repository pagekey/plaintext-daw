#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use std::sync::{Arc, Mutex};
use tauri::api::dialog;
use tauri::{Manager, State};

mod state;

struct AppState(Arc<Mutex<state::App>>);

fn render_song(path: String) {
    Command::new("plaintext-daw")
        .arg("render")
        .arg(path)
        .spawn()
        .expect("failed to render song");
}

#[tauri::command]
fn open_project(handle: tauri::AppHandle, app_state: State<AppState>) {
    let app_state = app_state.0.clone();
    dialog::FileDialogBuilder::new()
        .add_filter("Yaml", &["yml", "yaml"])
        .pick_file(move |file_path| {
            if let Some(path) = file_path {
                app_state.lock().unwrap().filepath = path.to_str().unwrap().to_string();
                tauri::WindowBuilder::new(
                    &handle,
                    "editor",
                    tauri::WindowUrl::App("index2.html".into()),
                )
                .title("Plaintext DAW Editor")
                .build()
                .unwrap();
                handle
                    .get_window("open-project")
                    .unwrap()
                    .close()
                    .expect("Unable to close window");
            }
        });
}

#[tauri::command]
fn get_app(handle: tauri::AppHandle, filepath: State<AppState>) -> state::App {
    let fpath = filepath.0.lock().unwrap();
    let result = (*fpath).clone();
    result
}

fn main() {
    tauri::Builder::default()
        .manage(AppState(Default::default()))
        .invoke_handler(tauri::generate_handler![get_app, open_project,])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
