#---------builder------------
FROM python:3.11-slim-bookworm as builder
WORKDIR /project

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# install rye
ENV RYE_HOME "/opt/rye"
ENV PATH "$RYE_HOME/shims:$PATH"
ENV RYE_NO_AUTO_INSTALL "1"
ENV RYE_INSTALL_OPTION "--yes" 
ENV RYE_TOOLCHAIN "/usr/local/bin/python"
RUN curl -sSf https://rye-up.com/get | bash

# config rye
RUN rye config --set-bool behavior.use-uv=true
RUN rye pin --relaxed 3

# install dependencies (no lockfile)
COPY pyproject.toml /project/
RUN rye sync --no-dev --all-features

# install dependencies (with lockfile)
# COPY pyproject.toml requirements.lock /project/
# RUN rye sync --no-dev --no-lock


#---------runner------------
FROM python:3.11-slim-bookworm as runner
WORKDIR /project

COPY --from=builder /project/.venv /project/.venv
ENV PATH /project/.venv/bin:$PATH

COPY src/app /project/app

ENV N_WORKERS 4

CMD uvicorn \
    --access-log \
    --host 0.0.0.0 \
    --port 8080 \
    --workers ${N_WORKERS} \
    app.server:app                              
