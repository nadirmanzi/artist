# --- Stage 0: Dev ---
FROM oven/bun:1.3-alpine AS dev
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
COPY . .
EXPOSE 5173
CMD ["bun", "run", "dev", "--", "--host", "0.0.0.0"]

# --- Stage 1: Dependencies ---
FROM oven/bun:1.3-alpine AS deps
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

# --- Stage 2: Build ---
FROM oven/bun:1.3-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN bun run build
RUN rm -rf node_modules && bun install --frozen-lockfile --production

# --- Stage 3: Runtime ---
FROM oven/bun:1.3-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=5173

RUN apk update && apk upgrade --no-cache \
  && apk add --no-cache tini \
  && addgroup -S svelte && adduser -S svelte -G svelte

COPY --from=builder --chown=svelte:svelte /app/build ./build
COPY --from=builder --chown=svelte:svelte /app/node_modules ./node_modules
COPY --from=builder --chown=svelte:svelte /app/package.json ./package.json

USER svelte
EXPOSE 5173

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD bun -e "fetch('http://localhost:5173').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["bun", "build/index.js"]