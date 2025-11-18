# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
FROM ghcr.io/astral-sh/uv:debian

ARG MY_UV_PYTHON_VERSION

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# Enable bytecode compilation
# Copy from the cache instead of linking since it's a mounted volume
# Only use the managed Python version
# Ensure installed tools can be executed out of the box
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_PREFERENCE=only-managed UV_TOOL_BIN_DIR=/usr/local/bin

# Install Python before the project for caching
RUN uv python install ${MY_UV_PYTHON_VERSION}

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=Makefile,target=Makefile \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    make setup-ci

COPY berserk ./berserk
# COPY uv.lock ./
# COPY pyproject.toml ./
# COPY Makefile ./
# COPY README.rst ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=Makefile,target=Makefile \
    --mount=type=bind,source=README.rst,target=README.rst \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    make setup

COPY integration/run-tests.sh ./integration/run-tests.sh
COPY integration/tests ./integration/tests

CMD ["./integration/run-tests.sh"]