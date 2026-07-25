import { listCatalogs } from '$lib/api/catalog/management';
import { createArtworkInquiry } from '$lib/api/inquiry/management'; // Adjust path if needed
import { error, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
    const res = await listCatalogs(fetch);

    if (!res.ok) {
        throw error(res.status || 500, res.error?.detail || 'Failed to load catalog');
    }

    return {
        catalog: res.data.catalogs
    };
};

export const actions: Actions = {
    inquire: async ({ request, fetch }) => {
        const formData = await request.formData();

        const catalog_id = formData.get('catalog_id')?.toString().trim();
        const name = formData.get('fullName')?.toString().trim();
        const email = formData.get('email')?.toString().trim();
        const phone = formData.get('phone')?.toString().trim();
        const message = formData.get('message')?.toString().trim() || '';

        // Server-side validation
        if (!catalog_id || !name || !email || !/^\S+@\S+\.\S+$/.test(email)) {
            return fail(400, {
                error: 'Please fill in all required fields.'
            });
        }

        const res = await createArtworkInquiry(
            {
                catalog_id,
                name,
                email,
                phone_number: phone || null,
                message // Ensures message is a string
            },
            fetch
        );

        if (!res.ok) {
            return fail(res.status || 500, {
                error: res.error?.detail || 'Failed to send artwork inquiry.'
            });
        }

        return { success: true };
    }
};