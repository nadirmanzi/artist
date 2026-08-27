<script lang="ts">
	import { page } from '$app/state';
	import Button from '$lib/components/ui/button/button.svelte';
	import Home from '@tabler/icons-svelte-runes/icons/home';
	import RotateClockwise from '@tabler/icons-svelte-runes/icons/rotate-clockwise';
	import Palette from '@tabler/icons-svelte-runes/icons/palette';
	import Artboard from '@tabler/icons-svelte-runes/icons/artboard';
	import School from '@tabler/icons-svelte-runes/icons/school';
	import Sparkles from '@tabler/icons-svelte-runes/icons/sparkles';
	import AlertTriangle from '@tabler/icons-svelte-runes/icons/alert-triangle';
	import ArrowLeft from '@tabler/icons-svelte-runes/icons/arrow-left';
	import { fade, fly, scale } from 'svelte/transition';

	type AccentKey = 'orange' | 'blue' | 'gold' | 'emerald' | 'violet';

	let activeAccentKey = $state<AccentKey>('orange');

	const accents: Record<AccentKey, { name: string; hex: string; glow: string; border: string }> = {
		orange: {
			name: 'Terracotta Orange',
			hex: '#ff6600',
			glow: 'rgba(255, 102, 0, 0.22)',
			border: 'rgba(255, 102, 0, 0.4)'
		},
		blue: {
			name: 'Ultramarine Blue',
			hex: '#0066ff',
			glow: 'rgba(0, 102, 255, 0.22)',
			border: 'rgba(0, 102, 255, 0.4)'
		},
		gold: {
			name: 'Studio Raw Gold',
			hex: '#e6a100',
			glow: 'rgba(230, 161, 0, 0.22)',
			border: 'rgba(230, 161, 0, 0.4)'
		},
		emerald: {
			name: 'Verdant Ochre',
			hex: '#10b981',
			glow: 'rgba(16, 185, 129, 0.22)',
			border: 'rgba(16, 185, 129, 0.4)'
		},
		violet: {
			name: 'Deep Violet Pigment',
			hex: '#8b5cf6',
			glow: 'rgba(139, 92, 246, 0.22)',
			border: 'rgba(139, 92, 246, 0.4)'
		}
	};

	const currentAccent = $derived(accents[activeAccentKey]);
	const status = $derived(page.status || 404);
	const is404 = $derived(status === 404);
	const isBackendError = $derived(status >= 500);

	const errorMessage = $derived(
		is404
			? 'The canvas or artwork you are looking for has left the frame, or has not been painted yet.'
			: isBackendError
				? 'The studio backend service is currently taking a pause or undergoing maintenance.'
				: page.error?.message
	);

	function reloadPage() {
		if (typeof window !== 'undefined') {
			window.location.reload();
		}
	}

	function goBack() {
		if (typeof window !== 'undefined' && window.history.length > 1) {
			window.history.back();
		} else {
			window.location.href = '/';
		}
	}
</script>

<svelte:head>
	<title>Studio Mugire — {status} {is404 ? 'Canvas Not Found' : 'Studio Error'}</title>
</svelte:head>

<div
	class="relative min-h-dvh w-full overflow-hidden bg-background text-white flex items-center justify-center px-4 py-16 selection:bg-white selection:text-black"
>
	<!-- Central Main Content Glass Card -->
	<div
		in:fly|global={{ y: 30, duration: 600 }}
		class="relative z-10 w-full max-w-2xl bg-transparent flex flex-col items-center text-center gap-6 overflow-hidden"
	>
		<!-- Top Gallery Tag / Status Badge -->
		<div
			class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/15 text-xs tracking-[0.2em] uppercase text-foreground font-medium"
		>
			<span class="size-2 rounded-full animate-pulse transition-colors bg-destructive duration-300"
			></span>
			<span>Studio Mugire • Ref #{status}</span>
		</div>

		<!-- Big Creative Display Number -->
		<div class="relative my-2">
			<h1
				class="font-display text-8xl sm:text-9xl font-extralight tracking-tighter text-transparent bg-clip-text bg-linear-to-b from-foreground via-foreground/90 to-foreground/20 select-none"
			>
				{status}
			</h1>

			<!-- Decorative Overlaid Brush Icon / Sparkle -->
			<div
				class="absolute -top-3 -right-4 p-2 text-destructive rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white/90 shadow-lg"
				in:scale|global={{ duration: 400, delay: 200 }}
			>
				{#if is404}
					<Sparkles class="size-6 sm:size-7 text-destructive" />
				{:else}
					<AlertTriangle class="size-6 sm:size-7 text-destructive" />
				{/if}
			</div>
		</div>

		<!-- Main Error Heading & Subtext -->
		<div class="space-y-3 max-w-lg text-foreground">
			<h2 class="font-display text-3xl sm:text-4xl font-normal leading-snug">
				{#if is404}
					Uncharted Canvassssss
				{:else if isBackendError}
					Atelier Connection Paused
				{:else}
					Studio Notice
				{/if}
			</h2>

			<p class="text-base sm:text-lg font-light text-surface-foreground-muted leading-relaxed">
				{errorMessage}
			</p>
		</div>

		<!-- Primary & Secondary Navigation Actions -->
		<div class="w-full pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
			{#if isBackendError}
				<Button
					onclick={reloadPage}
					variant="filled"
					color="black"
					size="lg"
					class="w-full sm:w-auto"
				>
					<RotateClockwise class="size-4" />
					<span>Retry Connection</span>
				</Button>
			{/if}

			<Button
				href="/"
				variant={isBackendError ? 'outline' : 'filled'}
				color="black"
				size="lg"
				class="w-full sm:w-auto"
			>
				<Home class="size-4" />
				<span>Return to Gallery</span>
			</Button>

			{#if is404}
				<Button href="/catalog" variant="outline" color="black" size="lg" class="w-full sm:w-auto">
					<Artboard class="size-4" />
					<span>Explore Collection</span>
				</Button>

				<Button href="/classes" variant="outline" color="black" size="lg" class="w-full sm:w-auto">
					<School class="size-4" />
					<span>Book a Class</span>
				</Button>
			{/if}
		</div>

		<!-- Back Link -->
		<div class="pt-2">
			<button
				type="button"
				onclick={goBack}
				class="inline-flex items-center gap-1.5 text-sm text-foreground transition-colors duration-200 cursor-pointer"
			>
				<ArrowLeft class="size-3.5" />
				<span>Return to previous page</span>
			</button>
		</div>
	</div>
</div>
