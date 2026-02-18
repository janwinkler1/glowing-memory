FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim@sha256:08252c0217a191047df9c8dc96f38a07f5a96d78f2b23f8145f8506aed0f6e11

RUN apt-get update && apt-get install -y --no-install-recommends cron && rm -rf /var/lib/apt/lists/*

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

RUN echo "00 7,16 * * * /bin/bash /app/src/run_script.sh > /proc/1/fd/1 2>&1" > /etc/cron.d/mycron \
    && chmod 0644 /etc/cron.d/mycron \
    && crontab /etc/cron.d/mycron \
    && touch /var/log/cron.log

CMD ["cron", "-f"]
