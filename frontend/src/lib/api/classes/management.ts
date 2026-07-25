import { apiFetch } from '../client';
import type { ClassBookingResponse, ClassListResponse } from '$lib/api/types';

export async function listClasses(customFetch: typeof fetch = fetch) {
    return apiFetch<ClassListResponse>('/classes/', {}, customFetch);
}

export async function bookClass(
    data: {
        program_id: string;
        name: string;
        email: string;
        phone_number?: string | null;
    },
    customFetch: typeof fetch = fetch
) {
    return apiFetch<ClassBookingResponse>(
        '/classes/bookings/v1/',
        {
            method: 'POST',
            body: JSON.stringify(data),
        },
        customFetch
    );
}
