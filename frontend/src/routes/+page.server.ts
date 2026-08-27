import { listCatalogs } from '$lib/api/catalog/management';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const res = await listCatalogs(fetch);

		if (!res.ok) {
			throw error(
				res.status || 500,
				res.error?.detail || 'The studio catalog service is currently unavailable.'
			);
		}

		return {
			catalogs: res.data?.catalogs ?? []
		};
	} catch (err: any) {
		if (err && typeof err === 'object' && 'status' in err) {
			throw err;
		}
		throw error(500, 'Unable to connect to the studio backend. Please check server connection.');
	}
};