# --- Stage 1: Full deps (for building) ---
FROM oven/bun:1.3.14-alpine AS deps
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

# --- Stage 2: Production-only deps (runs in parallel with builder below) ---
FROM oven/bun:1.3.14-alpine AS prod-deps
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile --production

# --- Stage 3: Builder ---
FROM oven/bun:1.3.14-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Public env vars are compiled into the client bundle at build time, so they
# must arrive as build args (from .env, via --build-arg or compose build.args),
# not as runtime ENV — by the time the container runs, the bundle is frozen.
ARG PUBLIC_BACKEND_URL
ENV PUBLIC_BACKEND_URL=${PUBLIC_BACKEND_URL}

RUN bun run build

# --- Stage 4: Production Runner ---
FROM oven/bun:1.3.14-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production \
    PORT=5173 \
    HOST=0.0.0.0

RUN apk update && apk upgrade --no-cache \
    && apk add --no-cache tini \
    && addgroup -S svelte && adduser -S svelte -G svelte

COPY --from=builder --chown=svelte:svelte /app/build ./build
COPY --from=prod-deps --chown=svelte:svelte /app/node_modules ./node_modules
COPY --from=builder --chown=svelte:svelte /app/package.json ./package.json

USER svelte
EXPOSE 5173

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD bun -e "fetch('http://localhost:5173').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["bun", "build/index.js"]
