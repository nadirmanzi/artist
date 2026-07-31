import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { env } from '$env/dynamic/public';


export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

export function formatPrice({
	price,
	currency = 'RWF'
}: {
	price: number | string;
	currency: 'RWF' | 'USD';
}) {
	return new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: currency
	}).format(Number(price));
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChild<T> = T extends { child?: any } ? Omit<T, 'child'> : T;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChildren<T> = T extends { children?: any } ? Omit<T, 'children'> : T;
export type WithoutChildrenOrChild<T> = WithoutChildren<WithoutChild<T>>;
export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & { ref?: U | null };

export function getImageUrl(imagePath?: string | null): string {
	if (!imagePath) return '';

	// Ensure fallback if env.PUBLIC_BACKEND_URL is undefined
	const publicBackend = (
		typeof env !== 'undefined' && env.PUBLIC_BACKEND_URL
			? env.PUBLIC_BACKEND_URL
			: 'http://localhost:8000'
	).replace(/\/$/, '');

	// If it's already an absolute URL
	if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
		try {
			const url = new URL(imagePath);
			// Replace internal container hostname ('backend') with public backend URL
			if (url.hostname === 'backend') {
				const targetUrl = new URL(publicBackend);
				url.protocol = targetUrl.protocol;
				url.hostname = targetUrl.hostname;
				url.port = targetUrl.port;
				return url.toString();
			}
			return imagePath;
		} catch {
			return imagePath;
		}
	}

	// Relative path
	const cleanPath = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;
	return `${publicBackend}${cleanPath}`;
}

