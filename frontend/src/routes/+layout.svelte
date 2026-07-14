<script lang="ts">
	import MainNavigation from '$lib/components/main-navigation.svelte';
	import { onNavigate } from '$app/navigation';
	import '../app.css';

	let { children } = $props();

	onNavigate((navigation) => {
		// If the user clicked a link to the exact same pathname,
		// cancel the view transition entirely.
		if (navigation.from?.url.pathname === navigation.to?.url.pathname) {
			return;
		}

		// Otherwise, allow the transition to trigger
		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
</script>

<header
	class="fixed w-screen z-[999] lg:p-4 flex items-center justify-center"
	style="view-transition-name: main-navigation;"
>
	<MainNavigation />

</header>

<main class="text-foreground w-screen min-h-dvh bg-background" id='main-container'>
	{@render children()}
</main>

<style>
	@keyframes scale-out-fade {
		from {
			opacity: 1;
			transform: scale(1);
		}
		to {
			opacity: 0;
			transform: scale(1.01);
		}
	}
	
	@keyframes scale-in-fade {
		from {
			opacity: 0;
			transform: scale(0.99);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* Outgoing content: accelerates out */
	:root::view-transition-old(root) {
		animation: 700ms cubic-bezier(0.4, 0, 1, 1) both scale-out-fade;
	}

	/* Incoming content: comes in hot, then decelerates to a soft settle */
	:root::view-transition-new(root) {
		animation: 900ms cubic-bezier(0, 0, 0.2, 1) both scale-in-fade;
		mix-blend-mode: normal;
	}

	/* Keep the header isolated and completely still */
	:root::view-transition-group(main-header) {
		animation: none;
	}
</style>
