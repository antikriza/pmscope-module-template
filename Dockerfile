FROM python:3.11-alpine
WORKDIR /app
RUN apk add --no-cache build-base
# Install vendored pmscope-sdk wheel first so module install can use --no-deps.
# See README.md "Vendored wheel" for refresh instructions when bumping pmscope-sdk.
COPY wheels/ ./wheels/
RUN pip install --no-cache-dir ./wheels/pmscope_sdk-0.1.0-py3-none-any.whl
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir --no-deps . && pip install --no-cache-dir uvicorn~=0.27.0
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget -q --spider http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
