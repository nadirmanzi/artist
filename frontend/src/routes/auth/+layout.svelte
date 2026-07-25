<script lang="ts">
	import { onNavigate } from '$app/navigation';
	import { page } from '$app/state';
	import Button from '$lib/components/ui/button/button.svelte';
	import ArrowLeft from '@tabler/icons-svelte-runes/icons/arrow-left';

	const { children } = $props();
	const is_login = $derived(page.url.pathname === '/auth/login');

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
</script>

<div class="h-dvh w-full">
	{@render children?.()}
</div>

<style>
	:root {
		view-transition-name: auth-layout;
	}

	::view-transition-old(root) {
		animation: 100ms ease-in both fade-out;
	}

	::view-transition-new(root) {
		animation: 100ms ease-out both fade-in;
	}

	@keyframes fade-out {
		from {
			opacity: 1;
		}
		to {
			opacity: 0;
		}
	}

	@keyframes fade-in {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
