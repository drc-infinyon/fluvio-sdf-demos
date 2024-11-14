FROM rust:1-slim-bookworm

# this build layer will built the rust binary
WORKDIR /app

COPY . .

RUN cargo build --release

# The final image layer will only have the viz2 binary in it
FROM rust:1-slim-bookworm

WORKDIR /app

COPY --from=0 /app/target/release/viz2 .

RUN apt-get update
RUN apt-get install -y curl unzip
RUN apt-get install -y tini openssl curl
RUN curl -fsS "https://hub.infinyon.cloud/install/install.sh?ctx=sdf-demo" | FLUVIO_VERSION=stable bash

ENV PATH "$PATH:/root/.fluvio/bin"
ENV PATH "$PATH:/root/.fvm/bin"

CMD ["/app/viz2"]

