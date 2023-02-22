#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use tauri_api::dialog;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
fn syscall_test() -> () {
    println!("hello tauri");
    Command::new("ls")
        .arg("-l")
        .arg("-a")
        .spawn()
        .expect("ls command failed to start");
    ()
}

#[tauri::command]
fn open_project() -> () {
    println!("Opening!");
    match dialog::select(Some(""), Some("")) {
        Ok(resp) => {
            match resp {
                dialog::Response::Okay(path) => {
                    println!("User chose {path}")
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
            println!("Open file faild")
        }
    }
}

pub fn add(a: i32, b: i32) -> i32 {
    return a + b;
}

#[test]
fn test_add() {
    let result = add(2, 3);
    assert_eq!(result, 5);
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .invoke_handler(tauri::generate_handler![syscall_test])
        .invoke_handler(tauri::generate_handler![open_project])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
