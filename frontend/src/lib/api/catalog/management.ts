import { apiFetch } from '../client';
import type { CatalogResponse, CatalogListResponse } from '$lib/api/types';


export async function listCatalogs(customFetch: typeof fetch = fetch) {
	return apiFetch<CatalogListResponse>('/catalog/management/', {}, customFetch);
}

export async function createCatalog(
	data: {
		name: string;
		description: string;
		price: number;
		category: string;
		dimensions: Record<string, any>;
		image: string;
		visibility_status: 'draft' | 'published' | 'archived';
	},
	customFetch: typeof fetch = fetch
) {
	return apiFetch<CatalogResponse>(
		'/catalog/management/',
		{
			method: 'POST',
			body: JSON.stringify(data)
		},
		customFetch
	);
}

export async function updateCatalog(catalogId: string, data: Partial<CatalogResponse>, customFetch: typeof fetch = fetch) {
	return apiFetch<CatalogResponse>(
		`/catalog/management/${catalogId}/`,
		{
			method: 'PATCH',
			body: JSON.stringify(data)
		},
		customFetch
	);
}

export async function deleteCatalog(catalogId: string, customFetch: typeof fetch = fetch) {
	return apiFetch<CatalogResponse>(
		`/catalog/management/${catalogId}/`,
		{
			method: 'DELETE'
		},
		customFetch
	);
}

export async function publishCatalog(catalogId: string, customFetch: typeof fetch = fetch) {
	return apiFetch<CatalogResponse>(
		`/catalog/management/${catalogId}/publish/`,
		{
			method: 'POST'
		},
		customFetch
	);
}

export async function archiveCatalog(catalogId: string, customFetch: typeof fetch = fetch) {
	return apiFetch<CatalogResponse>(
		`/catalog/management/${catalogId}/archive/`,
		{
			method: 'POST'
		},
		customFetch
	);
}

export async function draftCatalog(catalogId: string, customFetch: typeof fetch = fetch) {
	return apiFetch<CatalogResponse>(
		`/catalog/management/${catalogId}/draft/`,
		{
			method: 'POST'
		},
		customFetch
	);
}
