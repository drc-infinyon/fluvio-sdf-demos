
use poem::Route;
use poem::endpoint::StaticFilesEndpoint;
use poem::handler;

const STATIC_DIR: &str = "./static";

pub fn route() -> Route {
    Route::new().nest(
        "/stat",
        file_handler,
    )
}

pub fn index() -> Route {
    Route::new().nest(
        "/",
        StaticFilesEndpoint::new(STATIC_DIR).index_file("index.html"),
    )
}

#[handler]
async fn file_handler(req: &poem::Request) -> poem::Result<poem::Response> {
    let path = req.uri().path().trim_start_matches('/');

    let file_path = format!("{STATIC_DIR}/{}", path);
    if let Ok(contents) = tokio::fs::read(&file_path).await {
        let mime_type = mime_guess::from_path(&file_path).first_or_octet_stream();
        Ok(poem::Response::builder()
            .header("Content-Type", mime_type.as_ref())
            .body(contents)
            .into())
    } else {
        Ok(poem::Response::builder()
            .status(poem::http::StatusCode::NOT_FOUND)
            .body("File not found")
            .into())
    }
}