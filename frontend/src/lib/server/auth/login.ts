import { apiFetch } from '$lib/api/client';
import type { LoginResponse } from '$lib/api/types';
import type { RequestEvent } from '@sveltejs/kit';
import { forwardCookies } from '$lib/server/cookies';

/**
 * Standard Login Result.
 */
export interface LoginResult {
	success: boolean;
	user?: LoginResponse['user'];
	error?: string;
	code?: string;
	fieldErrors?: Record<string, string>;
}

/**
 * Authenticates user and manually forwards JWT cookies from Django to the Browser.
 */
export const login = async (
	email: string,
	password: string,
	customFetch: typeof fetch,
	event: RequestEvent
): Promise<LoginResult> => {
	const res = await apiFetch<LoginResponse>(
		'/users/auth/login/',
		{
			method: 'POST',
			body: JSON.stringify({ email, password })
		},
		customFetch
	);

	// --- COOKIE FORWARDING LOGIC ---
	if (res.headers) {
		forwardCookies(res.headers, event);
	}

	if (!res.ok) {
		const { error } = res;

		// Handle Field Validation
		if (Object.keys(error.errors).length > 0) {
			return {
				success: false,
				fieldErrors: {
					email: error.errors.email?.[0] || '',
					password: error.errors.password?.[0] || ''
				}
			};
		}

		return {
			success: false,
			code: error.code,
			error: error.detail || 'Authentication failed.'
		};
	}

	return {
		success: true,
		user: res.data.user
	};
};
