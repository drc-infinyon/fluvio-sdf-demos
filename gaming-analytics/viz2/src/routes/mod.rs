use poem::Route;

mod stat;
mod ws;

pub fn app_routes() -> Route {
    Route::new()
        .nest_no_strip("/", stat::index())
        .nest_no_strip("/stat", stat::route())
        .nest_no_strip("/ws", ws::route())
}
