import { apiFetch } from '../client';
import type {
	ArtworkInquiryListResponse,
	ArtworkInquiryResponse,
	ContactInquiryListResponse,
	ContactInquiryResponse,
	CreateArtworkInquiryRequest,
	CreateContactInquiryRequest,
	InquiryListResponse,
} from '$lib/api/types';

export async function listInquiries(customFetch: typeof fetch = fetch, authToken?: string) {
	return apiFetch<InquiryListResponse>('/catalog/management/inquiries/', { authToken }, customFetch);
}


export async function listContactInquiries(customFetch: typeof fetch = fetch, authToken?: string) {
	return apiFetch<ContactInquiryListResponse>('/inquiries/contact/', { authToken }, customFetch);
}

export async function createContactInquiry(
	data: CreateContactInquiryRequest,
	customFetch: typeof fetch = fetch
) {
	return apiFetch<ContactInquiryResponse>(
		'/inquiries/contact/',
		{
			method: 'POST',
			body: JSON.stringify(data)
		},
		customFetch
	);
}

export async function markContactInquiryAsRead(
	inquiryId: string,
	customFetch: typeof fetch = fetch,
	authToken?: string
) {
	return apiFetch<ContactInquiryResponse>(
		`/inquiries/contact/${inquiryId}/mark-read/`,
		{
			method: 'POST',
			authToken
		},
		customFetch
	);
}

export async function deleteContactInquiry(
	inquiryId: string,
	customFetch: typeof fetch = fetch,
	authToken?: string
) {
	return apiFetch<void>(
		`/inquiries/contact/${inquiryId}/`,
		{
			method: 'DELETE',
			authToken
		},
		customFetch
	);
}

export async function listArtworkInquiries(customFetch: typeof fetch = fetch, authToken?: string) {
	return apiFetch<ArtworkInquiryListResponse>('/inquiries/artwork/', { authToken }, customFetch);
}

export async function createArtworkInquiry(
	data: CreateArtworkInquiryRequest,
	customFetch: typeof fetch = fetch
) {
	return apiFetch<ArtworkInquiryResponse>(
		'/inquiries/artwork/',
		{
			method: 'POST',
			body: JSON.stringify(data)
		},
		customFetch
	);
}

export async function markArtworkInquiryAsRead(
	inquiryId: string,
	customFetch: typeof fetch = fetch,
	authToken?: string
) {
	return apiFetch<ArtworkInquiryResponse>(
		`/inquiries/artwork/${inquiryId}/mark-read/`,
		{
			method: 'POST',
			authToken
		},
		customFetch
	);
}

export async function deleteArtworkInquiry(
	inquiryId: string,
	customFetch: typeof fetch = fetch,
	authToken?: string
) {
	return apiFetch<void>(
		`/inquiries/artwork/${inquiryId}/`,
		{
			method: 'DELETE',
			authToken
		},
		customFetch
	);
}

export async function sendInquiry(
	data: CreateArtworkInquiryRequest,
	customFetch: typeof fetch = fetch
) {
	return createArtworkInquiry(data, customFetch);
}
