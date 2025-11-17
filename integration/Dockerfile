# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
FROM ghcr.io/astral-sh/uv:debian

# builder
ARG UV_CACHE_DIR

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=Makefile,target=Makefile \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    make setup-ci

COPY berserk ./berserk
# COPY uv.lock ./
# COPY pyproject.toml ./
# COPY Makefile ./
# COPY README.rst ./

RUN --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=Makefile,target=Makefile \
    --mount=type=bind,source=README.rst,target=README.rst \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    make setup

COPY integration ./integration

CMD ["./integration/run-tests.sh"]