import { listCatalogs } from '$lib/api/catalog/management'; // adjust path to your catalog api file
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
    const res = await listCatalogs(fetch);

    if (!res.ok) {
        return { catalogs: [] };
    }

    // res.data is CatalogListResponse ({ catalogs: Catalog[] })
    return {
        catalogs: res.data.catalogs
    };
};