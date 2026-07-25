import type { UserProfile } from '$lib/api/types';

declare global {
	namespace App {
		interface Locals {
			is_authenticated: boolean;
			user: UserProfile | null;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export { };
