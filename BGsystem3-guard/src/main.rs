#[warn(non_snake_case)]

use std::process::Command;
use std::os::windows::process::CommandExt;

const CREATE_NO_WINDOW: u32 = 0x08000000;

fn main() {
    let mut command = Command::new("cmd");
    command.args(&["/C", "target.bat"]);
    command.creation_flags(CREATE_NO_WINDOW);

    match command.spawn() {
        Ok(_) => println!("Batch file is running in the background."),
        Err(e) => eprintln!("Failed to run batch file: {}", e),
    }
}