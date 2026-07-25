import { error, fail } from '@sveltejs/kit';
import { listClasses, bookClass } from '$lib/api/classes/management'; // Adjust import path as needed
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
    const res = await listClasses(fetch);

    if (!res.ok) {
        throw error(res.status || 500, res.error?.detail || 'Failed to load classes');
    }

    return {
        classes: res.data.classes,
    };
};

export const actions: Actions = {
    book: async ({ request, fetch }) => {
        const formData = await request.formData();

        const program_id = formData.get('catalog_id')?.toString().trim(); // Sent from page.svelte hidden input
        const name = formData.get('fullName')?.toString().trim();
        const email = formData.get('email')?.toString().trim();
        const phone = formData.get('phone')?.toString().trim();

        // Server-side validation
        if (!program_id || !name || !email || !/^\S+@\S+\.\S+$/.test(email)) {
            return fail(400, {
                error: 'Please complete all required fields correctly.'
            });
        }

        const res = await bookClass(
            {
                program_id,
                name,
                email,
                phone_number: phone || null,
            },
            fetch
        );

        if (!res.ok) {
            return fail(res.status || 500, {
                error: res.error?.detail || 'Failed to complete class booking.'
            });
        }

        return { success: true };
    }
};