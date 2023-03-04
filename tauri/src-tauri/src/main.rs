#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use std::sync::Mutex;
use tauri::State;
use tauri_api::dialog;

mod state;

struct AppState(Mutex<state::App>);

fn render_song(path: String) {
    Command::new("plaintext-daw")
        .arg("render")
        .arg(path)
        .spawn()
        .expect("failed to render song");
}

#[tauri::command]
fn open_project(handle: tauri::AppHandle, app_state: State<AppState>) -> () {
    match dialog::select(Some("yml, yaml"), Some(".")) {
        Ok(resp) => {
            match resp {
                dialog::Response::Okay(path) => {
                    let mut app_state_ref = app_state.0.lock().unwrap();
                    let pth = &(*app_state_ref).filepath;
                    println!("old path: {pth}");
                    (*app_state_ref).filepath = path;
                    let path = &(*app_state_ref).filepath;
                    println!("Set new path {path}");
                    tauri::WindowBuilder::new(
                        &handle,
                        "editor",
                        tauri::WindowUrl::App("index2.html".into())
                    ).title("Plaintext DAW Editor")
                    .build().unwrap();
                }
                dialog::Response::OkayMultiple(paths) => {
                    println!("Multiple paths: {:?}", paths)
                }
                dialog::Response::Cancel => {
                    println!("Cancel")
                }
            }
        }
        Err(_) => {
            println!("Open file failed")
        }
    }
}

#[tauri::command]
fn get_filepath(handle: tauri::AppHandle, filepath: State<AppState>) -> String {
    let fpath = filepath.0.lock().unwrap();
    let result = (*fpath).clone().filepath;
    println!("Got result: {result}");
    result
}

fn main() {
    tauri::Builder::default()
        .manage(AppState(Default::default()))
        .invoke_handler(tauri::generate_handler![
            get_filepath,
            open_project,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
