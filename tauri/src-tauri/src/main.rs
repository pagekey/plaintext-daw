#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use std::sync::Mutex;
use tauri::State;
use tauri_api::dialog;

struct Filepath(Mutex<String>);

fn render_song(path: String) {
    Command::new("plaintext-daw")
        .arg("render")
        .arg(path)
        .spawn()
        .expect("failed to render song");
}

#[tauri::command]
fn open_project(handle: tauri::AppHandle, filepath: State<Filepath>) -> () {
    match dialog::select(Some("yml, yaml"), Some(".")) {
        Ok(resp) => {
            match resp {
                dialog::Response::Okay(path) => {
                    let mut pth = filepath.0.lock().unwrap();
                    println!("old path: {pth}");
                    *pth = path;
                    println!("Set new path {pth}");
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
fn get_filepath(handle: tauri::AppHandle, filepath: State<Filepath>) -> String {
    let fpath = filepath.0.lock().unwrap();
    let result = (*fpath).clone();
    println!("Got result: {result}");
    result
}

fn main() {
    tauri::Builder::default()
        .manage(Filepath(Default::default()))
        .invoke_handler(tauri::generate_handler![
            get_filepath,
            open_project,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
