import { refreshToken, getUserProfile } from '$lib/server/auth/session';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

export const handle: Handle = async ({ event, resolve }) => {
    let access_token = event.cookies.get('access_token');
    const refresh_token = event.cookies.get('refresh_token');
    const access_token_expires = event.cookies.get('access_token_expires');

    const now = Math.floor(Date.now() / 1000);
    // Add 60s buffer to prevent edge-case race conditions with token expiry
    // If the expiry cookie is missing, default to true to trigger self-healing
    const is_expired = access_token_expires ? parseInt(access_token_expires) <= (now + 60) : true;

    // ─── 1. AUTO-REFRESH LOGIC (Section 7) ────────────────────────────────────
    // If we have a refresh token and the access token is missing or expired,
    // attempt to rotate the tokens.
    if (refresh_token && (!access_token || is_expired)) {
        const refreshed = await refreshToken(event);

        if (refreshed) {
            // New tokens were set by the refresh request
            access_token = event.cookies.get('access_token');
        } else {
            // Rotation failed, invalid session
            event.cookies.delete('access_token', { path: '/' });
            event.cookies.delete('refresh_token', { path: '/' });
            event.cookies.delete('access_token_expires', { path: '/' });
            event.locals.is_authenticated = false;
            event.locals.user = null;
            return resolve(event);
        }
    }

    if (!access_token) {
        event.locals.is_authenticated = false;
        event.locals.user = null;
        return resolve(event);
    }

    // ─── 2. SESSION VALIDATION & IDENTITY ───────────────────────────────────
    // We fetch the full profile to ensure the session is still valid (session_version Check)
    // and to correctly set the password_expired state in locals.
    const user = await getUserProfile(event.fetch, access_token);

    if (!user) {
        // Token might be valid but session revoked or user deleted
        event.cookies.delete('access_token', { path: '/' });
        event.cookies.delete('refresh_token', { path: '/' });
        event.cookies.delete('access_token_expires', { path: '/' });
        event.locals.is_authenticated = false;
        event.locals.user = null;
        return resolve(event);
    }

    // Populate locals with full profile
    event.locals.is_authenticated = true;
    event.locals.user = user;

    return resolve(event);
};

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
    // Automatically attach the Bearer token to all internal server-side fetches targeting the backend
    if (request.url.startsWith(PUBLIC_BACKEND_URL || '')) {
        const access_token = event.cookies.get('access_token');
        if (access_token && !request.headers.has('Authorization')) {
            request.headers.set('Authorization', `Bearer ${access_token}`);
        }
    }
    return fetch(request);
};
