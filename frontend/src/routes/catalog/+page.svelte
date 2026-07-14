<script lang="ts">
	import AnimatedPillGroup from '$lib/components/ui/animated-pill/animated-pill-group.svelte';
	import AnimatedPillItem from '$lib/components/ui/animated-pill/animated-pill-item.svelte';
	import { Button } from '$lib/components/ui/button';
	import ArrowRight from '@tabler/icons-svelte-runes/icons/arrow-right';
	import ChevronDown from '@tabler/icons-svelte-runes/icons/chevron-down';

	const categories = $state([
		{ name: 'All', href: '/catalog' },
		{ name: 'Mixed Media', href: '/catalog/mixed-media' },
		{ name: 'Landscapes', href: '/catalog/landscapes' },
		{ name: 'Portraits', href: '/catalog/portraits' }
	]);

	const catalog = $state([
		{
			name: 'Whispers of the Coast',
			category: 'Landscapes',
			dimensions: '24" x 36"',
			price: '1,200',
			image: '/art-1.jpeg'
		},
		{
			name: 'Echoes of Gold',
			category: 'Mixed Media',
			dimensions: '18" x 24"',
			price: '850',
			image: '/art-2.jpeg'
		},
		{
			name: "The Guardian's Gaze",
			category: 'Portraits',
			dimensions: '30" x 30"',
			price: '1,650',
			image: '/art-1.jpeg'
		},
		{
			name: 'Neon Metropolis',
			category: 'Mixed Media',
			dimensions: '36" x 48"',
			price: '2,100',
			image: '/art-2.jpeg'
		},
		{
			name: 'Silent Valley',
			category: 'Landscapes',
			dimensions: '16" x 20"',
			price: '650',
			image: '/art-1.jpeg'
		},
		{
			name: 'Serenade in Blue',
			category: 'Portraits',
			dimensions: '20" x 24"',
			price: '950',
			image: '/art-2.jpeg'
		}
	]);

	let selectedCategory = $state('All');
</script>

<svelte:head>
	<title>Catalog</title>
</svelte:head>

<div class="h-[30dvh] bg-surface w-full flex flex-col justify-end px-20">
	<div class="py-10">
		<p class="text-surface-foreground-muted text-sm">Catalog</p>
		<p class="font-display text-5xl">Masterpieces by David</p>
	</div>
</div>

<div class="px-20 py-20 flex flex-col space-y-20 bg-background">
	<div class="flex items-center justify-between w-full">
		<div class="bg-surface rounded-full p-2 border w-fit border-black/20">
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

		<div class="flex items-center space-x-4 text-sm">
			<p class="text-surface-foreground-muted">Sort by:</p>
			<span class="px-3 flex items-center space-x-4 py-2 border border-black/20 rounded-lg bg-surface">
				<p class="">Newest</p>
				<ChevronDown class="size-5" />
			</span>
		</div>
	</div>

	<div class="p-1 grid-cols-3 gap-x-8 gap-y-20 grid">
		{#each catalog as artwork, index (artwork.name)}
			<div
				class={`space-y-6 pb-10 ${index < catalog.length - (catalog.length % 3 || 3) ? 'border-b border-black/30' : ''}`}
			>
				<img src={artwork.image} alt={artwork.name} class="h-[35rem] w-full object-cover" />
				<div class="">
					<p class="font-display font-semibold text-xl">{artwork.name}</p>
					<div class="py-4 space-y-2 text-surface-foreground-muted">
						<p>{artwork.category}</p>
						<p>{artwork.dimensions}</p>
					</div>

					<div class="flex items-center justify-between">
						<p class="font-semibold">USD {artwork.price}</p>

						<Button color="black" variant="tonal" size="sm" class="">Inquire <ArrowRight /></Button>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>

<div class="px-10 py-20 border-t border-black/10 bg-foreground text-white">
	<div class="flex items-center justify-evenly">
		<div class="space-y-6">
			<p class="text-4xl font-display font-medium">Don't see what you're looking for?</p>
			<p class="text-nav-foreground-muted text-sm">
				Studio Mugire accepts a limited number of commissions each year. <br /> Reach out to discuss a
				custom work made specifically for your space.
			</p>
		</div>

		<Button color="white" class="" size="lg">REQUEST A COMMISSION</Button>
	</div>
</div>
