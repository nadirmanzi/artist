<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import { animate } from '$lib/utils/animate';
	import ArrowLeft from '@tabler/icons-svelte-runes/icons/arrow-left';
	import ArrowRight from '@tabler/icons-svelte-runes/icons/arrow-right';
	import Compass from '@tabler/icons-svelte-runes/icons/compass';
	import * as Carousel from '$lib/components/ui/carousel';

	import HeroImage from '$lib/assets/hero-image.jpg';
	import HeroImage2 from '$lib/assets/hero-image7.jpg';

	const carouselImages = $state([
		{
			img: HeroImage,
			url: '#'
		},
		{
			img: HeroImage2,
			url: '#'
		},
	])
</script>

<svelte:head>
  <title>Studio Mugire</title>
</svelte:head>

<div class="h-dvh max-h-dvh w-screen overflow-hidden relative">
	<div class="h-full w-full overflow-hidden">
		<Carousel.Root class="h-full w-full relative">
			<Carousel.Content class="h-full flex">

				{#each carouselImages as image (image.img)}
					<Carousel.Item class="h-full min-w-0 shrink-0 w-full">
						<div class="h-full w-full overflow-hidden">
							<img src={image.img} alt="Hero image" class="w-full h-full object-cover block" />
						</div>
					</Carousel.Item>
					
				{/each}
				

			</Carousel.Content>

			<div
				class="absolute top-1/2 -translate-y-1/2 left-0 w-full flex justify-between px-4 z-20 pointer-events-none"
			>
				<Carousel.Previous class="mx-20 p-2 bg-foreground text-white border-0" />
				<Carousel.Next class="mx-20 p-2 bg-foreground text-white border-0" />
			</div>
		</Carousel.Root>
	</div>

	<div
		id="hero-text"
		use:animate={{ type: 'from', opacity: 0, y: 50, duration: 0.5 }}
		class="flex flex-col leading-[1.1] text-[6rem] font-bold mix-blend-difference text-white absolute font-display top-10 left-10 pointer-events-none"
	>
		<p>
			Art that <span>speaks</span>
		</p>
		<p class="pl-40 text-transparent [-webkit-text-stroke:2px_var(--color-surface)]">
			without words
		</p>
	</div>

	<div class="absolute right-14 top-14 z-10">
		<a
			href="#"
			class="underline flex items-center justify-center text-sm font-semibold space-x-2 underline-offset-6 hover:decoration-wavy transition-all duration-200 ease-in-out text-white"
		>
			<p>Explore artwork</p>
			<Compass stroke-width={1.5} class="size-5" />
		</a>
	</div>
</div>
