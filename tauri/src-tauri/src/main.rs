#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use tauri_api::dialog;

#[tauri::command]
fn open_project(handle: tauri::AppHandle) -> () {
    println!("Opening!");
    match dialog::select(Some("yml, yaml"), Some(".")) {
        Ok(resp) => {
            match resp {
                dialog::Response::Okay(path) => {
                    println!("User chose {path}");
                    Command::new("plaintext-daw")
                        .arg("render")
                        .arg(path)
                        .spawn()
                        .expect("failed to render song");
                    println!("Rendered song");
                    tauri::WindowBuilder::new(
                        &handle,
                        "editor",
                        tauri::WindowUrl::App("index2.html".into())
                    ).build().unwrap();
                }
                dialog::Response::OkayMultiple(paths) => {
                    println!("Multiple paths: {:?}", paths)
                }
                dialog::Response::Cancel => {
                    println!("Cancel")
                }
            }
            println!("Success file open")
        }
        Err(_) => {
            println!("Open file failed")
        }
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![open_project])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
