import { apiFetch } from '$lib/api/client';
import type { RequestEvent } from '@sveltejs/kit';
import { forwardCookies } from '$lib/server/cookies';

/**
 * Logs the user out and invalidates the session on the backend.
 * Section 3.5 of API Guide.
 */
export const logout = async (event: RequestEvent): Promise<boolean> => {
	const access_token = event.cookies.get('access_token');
	const refresh_token = event.cookies.get('refresh_token');

	const { ok, headers } = await apiFetch(
		'/users/auth/logout/',
		{
			method: 'POST',
			authToken: access_token,
			refreshCookie: refresh_token
		},
		event.fetch
	);

	// Forward the backend's deletion cookies (if any)
	if (headers) {
		forwardCookies(headers, event);
	}

	// Always clear local cookies to ensure immediate client-side logout
	event.cookies.delete('access_token', { path: '/' });
	event.cookies.delete('refresh_token', { path: '/' });
	event.cookies.delete('access_token_expires', { path: '/' });

	return ok;
};
