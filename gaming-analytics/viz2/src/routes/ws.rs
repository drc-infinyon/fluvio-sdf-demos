
use fluvio::{
    Fluvio,
    consumer::ConsumerConfigExtBuilder,
    Offset,
};
use futures_util::{SinkExt, StreamExt};
use poem::{
    get, handler,
    web::{
        websocket::{Message, WebSocket},
        Path,
    },
    EndpointExt, IntoResponse, Route,
};


pub fn route() -> Route {
    Route::new().at(
        "/ws/:name",
        get(ws.data(tokio::sync::broadcast::channel::<String>(32).0)),
    )
}



#[handler]
async fn ws(
    Path(name): Path<String>,
    ws: WebSocket,
) -> impl IntoResponse {
    tracing::info!("ws connect /ws/{name}");
    ws.on_upgrade(move |mut socket| async move {
        let fluvio = Fluvio::connect().await
        .expect("couldn't connect to fluvio");

        let cfg = ConsumerConfigExtBuilder::default()
            .topic(name)
            .offset_start(Offset::beginning())
            .build()
            .expect("couldn't config");

        let mut fl_stream = fluvio.consumer_with_config(cfg)
            .await
            .expect("Couldn't start fluvio stream");

        tokio::spawn(async move {
            while let Some(Ok(rec)) = fl_stream.next().await {
                let rec: String = String::from_utf8_lossy(rec.value().as_ref()).into_owned();
                let msg: Message = Message::Text(rec);
                if socket.send(msg).await.is_err() {
                    break;
                }
            }
        });
    })
}
