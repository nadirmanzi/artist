<script lang="ts">
	import { enhance } from '$app/forms';
	import { fade, fly } from 'svelte/transition';
	import AnimatedPillGroup from '$lib/components/ui/animated-pill/animated-pill-group.svelte';
	import AnimatedPillItem from '$lib/components/ui/animated-pill/animated-pill-item.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import Input from '$lib/components/ui/input.svelte';
	import ArrowRight from '@tabler/icons-svelte-runes/icons/arrow-right';
	import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';
	import { formatPrice, getImageUrl } from '$lib/utils.js';
	import CatalogCard from '$lib/components/catalog-card.svelte';
	import EmptyState from '$lib/components/empty-state.svelte';
	import Artboard from '@tabler/icons-svelte-runes/icons/artboard';

	let { data } = $props();

	const categories = $state([
		{ name: 'All'  },
		{ name: 'Landscapes' },
		{ name: 'Portraits' },
		{ name: 'Mixed Media' },
	]);

	let catalog = $derived(data.catalog ?? []);
	let selectedCategory = $state('All');

	// Filtered view according to selected category pill
	let filteredCatalog = $derived(
		selectedCategory === 'All'
			? catalog
			: catalog.filter((item) => item.category === selectedCategory)
	);

</script>

<svelte:head>
	<title>Catalog</title>
</svelte:head>

<div class="h-[30dvh] bg-surface w-full flex flex-col justify-end px-6 sm:px-12 md:px-20">
	<div class="py-10">
		<p class="font-display text-3xl sm:text-4xl md:text-5xl">Artworks by David Mugire Peace</p>
	</div>
</div>

<div
	class="px-6 sm:px-12 md:px-20 py-10 md:py-20 flex flex-col space-y-10 md:space-y-20 bg-background"
>
	<div class="flex items-center justify-between w-full overflow-x-auto pb-2 md:pb-0">
		<div class="bg-surface rounded-full p-2 border w-fit border-black/20 shrink-0">
			<AnimatedPillGroup color="var(--color-foreground)" direction="horizontal">
				{#each categories as category (category.name)}
					<AnimatedPillItem
						class={`py-2 px-4 text-sm hover:text-white ${category.name === selectedCategory ? ' text-white' : ''}`}
						active={category.name === selectedCategory}
						onclick={() => (selectedCategory = category.name)}
					>
						<p>{category.name}</p>
					</AnimatedPillItem>
				{/each}
			</AnimatedPillGroup>
		</div>
	</div>

	<div class="p-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12 md:gap-y-20">
		{#each filteredCatalog as artwork, index (artwork.catalog_id ?? artwork.name)}
			<CatalogCard {artwork} {index} />
		{:else}
			<EmptyState
				title="No Artworks Found"
				description={selectedCategory === 'All'
					? 'There are currently no items available in the catalog. Check back soon for new additions.'
					: `No pieces currently match the "${selectedCategory}" category.`}
				icon={Artboard}
				class="col-span-full"
			>
				{#snippet action()}
					{#if selectedCategory !== 'All'}
						<Button
							color="black"
							variant="outline"
							size="sm"
							onclick={() => (selectedCategory = 'All')}
						>
							View All Artworks
						</Button>
					{/if}
				{/snippet}
			</EmptyState>
		{/each}
	</div>
</div>

<div class="px-6 md:px-10 py-12 md:py-20 border-t border-surface-border bg-foreground text-white">
	<div
		class="flex flex-col md:flex-row items-start md:items-center justify-between lg:justify-evenly gap-8 md:gap-0"
	>
		<div class="space-y-4 md:space-y-6">
			<p class="text-2xl sm:text-3xl md:text-4xl font-display font-medium">
				Don't see what you're looking for?
			</p>
			<p class="text-nav-foreground-muted text-sm">
				Studio Mugire accepts a limited number of commissions each year. <br
					class="hidden sm:block"
				/> Reach out to discuss a custom work made specifically for your space.
			</p>
		</div>

		<Button color="white" size="lg" class="w-full md:w-auto" href="/contacts"
			>REQUEST A COMMISSION</Button
		>
	</div>
</div>
