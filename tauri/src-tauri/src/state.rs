use serde::Serialize;

#[derive(Clone, Default, Serialize)]
pub struct App {
    pub filepath: String,
    pub contents: String,
}
