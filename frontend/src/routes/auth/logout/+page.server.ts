import type { Actions } from './$types';
import { logout } from '$lib/server/auth/users/logout';
import { redirect } from '@sveltejs/kit';

export const actions: Actions = {
	default: async (event) => {
		await logout(event);
		return redirect(302, '/auth/login');
	}
};
