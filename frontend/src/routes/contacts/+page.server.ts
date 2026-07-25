import { fail } from '@sveltejs/kit';
import { createContactInquiry } from '$lib/api/inquiry/management'; // Adjust import path as needed
import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, fetch }) => {
        const formData = await request.formData();

        const name = formData.get('name')?.toString().trim();
        const email = formData.get('email')?.toString().trim();
        const phone = formData.get('phone')?.toString().trim();
        const message = formData.get('message')?.toString().trim();

        // Server-side Validation
        if (!name || !email || !message) {
            return fail(400, {
                error: 'Please fill in all required fields.',
                values: { name, email, phone, message }
            });
        }

        if (!/^\S+@\S+\.\S+$/.test(email)) {
            return fail(400, {
                error: 'Please enter a valid email address.',
                values: { name, email, phone, message }
            });
        }

        // Call backend API
        const res = await createContactInquiry(
            {
                name,
                email,
                phone: phone || null,
                message
            },
            fetch
        );

        if (!res.ok) {
            return fail(res.status || 500, {
                error: res.error?.detail || 'Failed to submit inquiry. Please try again later.',
                values: { name, email, phone, message }
            });
        }

        return { success: true };
    }
};