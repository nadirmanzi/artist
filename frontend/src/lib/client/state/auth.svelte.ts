import type { UserProfile } from '$lib/api/types';

interface AuthState {
	is_authenticated: boolean;
	user: UserProfile | null;
}

export const auth_state: AuthState = $state({
	is_authenticated: false,
	user: null
});

export const setAuth = (user: UserProfile) => {
	auth_state.is_authenticated = true;
	auth_state.user = user;
};

export const revokeAuth = () => {
	auth_state.is_authenticated = false;
	auth_state.user = null;
};
