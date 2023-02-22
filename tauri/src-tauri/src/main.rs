#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
fn syscall_test() -> () {
    println!("hello tauri");
    ()
}

pub fn add(a: i32, b: i32) -> i32 {
    return a + b;
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .invoke_handler(tauri::generate_handler![syscall_test])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[test]
fn test_add() {
    let result = add(2, 3);
    assert_eq!(result, 5);
}
