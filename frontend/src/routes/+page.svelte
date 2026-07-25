<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	import ArrowDown from '@tabler/icons-svelte-runes/icons/arrow-down';

	import Compass from '@tabler/icons-svelte-runes/icons/compass';
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input.svelte';
	import * as Carousel from '$lib/components/ui/carousel';
	import { animate } from '$lib/utils/animate';
	import { gsap } from 'gsap';
	import type { PageData } from './$types';

	import HeroImage from '$lib/assets/hero-3.jpeg';
	import HeroImage2 from '$lib/assets/art-2.jpeg';

	let { data }: { data: PageData } = $props();

	const carouselImages = $state([
		{ img: HeroImage2, alt: 'Abstract artwork 1' },
		{ img: HeroImage, alt: 'Abstract artwork 2' }
	]);

	const featuredWork = $derived((data.catalogs ?? []).slice(0, 4));

	const commissionSteps = [
		{
			title: 'Consultation',
			copy: 'We talk mood, scale, and the architectural space it will inhabit.'
		},
		{ title: 'Concept', copy: 'Color studies and initial direction return for your feedback.' },
		{ title: 'Creation', copy: 'Built in layers over 3–5 weeks with milestone photo updates.' },
		{ title: 'Delivery', copy: 'Crated, insured, and delivered directly to your doorstep.' }
	];

	// Magnetic tilt for featured work cards — cursor-driven, purely additive.
	function tiltCard(e: MouseEvent) {
		const card = e.currentTarget as HTMLElement;
		const rect = card.getBoundingClientRect();
		const px = (e.clientX - rect.left) / rect.width;
		const py = (e.clientY - rect.top) / rect.height;

		gsap.to(card, {
			rotateX: (py - 0.5) * -12,
			rotateY: (px - 0.5) * 12,
			scale: 1.03,
			duration: 0.5,
			ease: 'power2.out',
			transformPerspective: 700,
			transformOrigin: 'center'
		} as gsap.TweenVars);
	}

	function resetCard(e: MouseEvent) {
		gsap.to(
			e.currentTarget as HTMLElement,
			{
				rotateX: 0,
				rotateY: 0,
				scale: 1,
				duration: 0.7,
				ease: 'power3.out'
			} as gsap.TweenVars
		);
	}
</script>

<svelte:head>
	<title>Studio Mugire — Fine Art & Commissions</title>
</svelte:head>

<!-- ==========================================
     A. HERO — parallax scrub + on-load entrance
     ========================================== -->
<div class="relative h-[100dvh] w-full overflow-hidden bg-black">
	<div
		class="absolute inset-0 z-0 h-full w-full"
		use:animate={{
			type: 'to',
			scale: 1.25,
			yPercent: 8,
			ease: 'none',
			scrollTrigger: {
				start: 'top top',
				end: 'bottom top',
				scrub: true
			}
		}}
	>
		<Carousel.Root class="h-full w-full" opts={{ loop: true }}>
			<Carousel.Content class="h-full">
				{#each carouselImages as image (image.img)}
					<Carousel.Item class="h-[100dvh] w-full shrink-0 pl-0">
						<div class="h-full w-full overflow-hidden">
							<img
								src={image.img}
								alt={image.alt}
								class="block h-full w-full select-none object-cover"
							/>
						</div>
					</Carousel.Item>
				{/each}
			</Carousel.Content>

			<Carousel.Previous
				class="absolute left-4 top-1/2 z-30 -translate-y-1/2 border-none bg-black/60 p-3 text-white hover:bg-black/80 sm:left-8"
			/>
			<Carousel.Next
				class="absolute right-4 top-1/2 z-30 -translate-y-1/2 border-none bg-black/60 p-3 text-white hover:bg-black/80 sm:right-8"
			/>
		</Carousel.Root>
	</div>

	<!-- Vignette darkens further as you scrub down the hero -->
	<div
		class="pointer-events-none absolute inset-0 z-10 bg-linear-to-t from-black via-black/5 to-transparent"
		use:animate={{
			type: 'to',
			opacity: 1.6,
			ease: 'none',
			scrollTrigger: {
				start: 'top top',
				end: 'bottom top',
				scrub: true
			}
		}}
	></div>

	<!-- Hero text: fades/lifts on load, then scrubs away (parallax exit) as you scroll -->
	<div
		class="pointer-events-none absolute bottom-25 left-1/2 -translate-x-1/2 inset-0 z-20 flex flex-col justify-end items-center text-center text-white"
		use:animate={{
			type: 'to',
			yPercent: -20,
			opacity: 0,
			ease: 'none',
			scrollTrigger: {
				start: 'top top',
				end: '60% top',
				scrub: true
			}
		}}
	>
		<h1
			class="font-display text-5xl font-thin tracking-tight text-nowrap sm:text-5xl md:text-6xl lg:text-7xl text-white"
			use:animate={{
				type: 'from',
				opacity: 0,
				y: 70,
				scale: 1.5,
				skewY: 3,
				duration: 1,
				ease: 'power4.out',
				delay: 0.35
			}}
		>
			Studio Mugire
		</h1>

		<p
			class="mt-8 text-xs font-semibold tracking-[0.3em] uppercase text-white/80"
			use:animate={{
				type: 'from',
				opacity: 0,
				y: 16,
				duration: 0.6,
				ease: 'power2.out',
				delay: 0.15
			}}
		>
			Contemporary Art Studio & Gallery
		</p>
	</div>

	<div
		class="absolute bottom-6 left-1/2 z-30 flex -translate-x-1/2 flex-col items-center gap-2 text-white/80"
		use:animate={{
			type: 'from',
			opacity: 0,
			duration: 0.6,
			ease: 'power2.out',
			delay: 1.1
		}}
	>
		<span class="text-[10px] font-medium tracking-[0.2em] uppercase">Scroll</span>
		<ArrowDown class="size-4 animate-bounce" />
	</div>
</div>

<!-- ==========================================
     B. ETHOS — clip-path reveal scrubbed to scroll
     ========================================== -->
<section class="mx-auto max-w-7xl overflow-hidden px-4 py-24 sm:px-8 lg:px-16 lg:py-36">
	<div class="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-16">
		<div
			class="lg:col-span-7"
			use:animate={{
				type: 'from',
				opacity: 0,
				y: 80,
				scale: 0.95,
				clipPath: 'inset(0 0 100% 0)',
				ease: 'none',
				scrollTrigger: {
					start: 'top 95%',
					end: 'top 45%',
					scrub: true
				}
			}}
		>
			<p class="mb-4 text-xs font-bold tracking-[0.2em] uppercase text-muted-foreground">
				Our Philosophy
			</p>
			<h2 class="font-display text-3xl font-bold leading-tight sm:text-5xl lg:text-6xl">
				Art designed to hold space in modern interiors.
			</h2>
		</div>

		<div
			class="flex flex-col justify-end lg:col-span-5"
			use:animate={{
				type: 'from',
				opacity: 0,
				y: 60,
				ease: 'none',
				scrollTrigger: {
					start: 'top 90%',
					end: 'top 40%',
					scrub: true
				}
			}}
		>
			<p class="text-base leading-relaxed text-muted-foreground sm:text-lg">
				Studio Mugire produces limited fine art pieces and client commissions focused on scale,
				physical texture, and minimalist form. Every work is crafted with archival mediums in our
				local studio.
			</p>
		</div>
	</div>
</section>

<!-- ==========================================
     D. THE ARTIST — pinned-feel scrub zoom + skew
     ========================================== -->

<div class="bg-surface w-full overflow-hidden">
	<section class="mx-auto max-w-7xl overflow-hidden px-4 py-24 sm:px-8 lg:px-16 lg:py-36">
		<div class="grid grid-cols-1 items-center gap-12 lg:grid-cols-12 lg:gap-16">
			<div
				class="relative overflow-hidden rounded-3xl lg:col-span-6"
				use:animate={{
					type: 'from',
					scale: 1.3,
					rotate: 4,
					opacity: 0.2,
					ease: 'none',
					scrollTrigger: {
						start: 'top 100%',
						end: 'top 30%',
						scrub: true
					}
				}}
			>
				<img
					src="/images/mugire.jpeg"
					alt="David Mugire working in the studio"
					class="aspect-[4/5] w-full object-cover"
				/>
			</div>

			<div
				class="flex flex-col gap-6 lg:col-span-6"
				use:animate={{
					type: 'from',
					x: 80,
					opacity: 0,
					ease: 'none',
					scrollTrigger: {
						start: 'top 95%',
						end: 'top 45%',
						scrub: true
					}
				}}
			>
				<span class="text-xs font-bold tracking-[0.2em] uppercase text-muted-foreground">
					Behind the Canvas
				</span>
				<h2 class="font-display text-3xl font-bold sm:text-5xl">David Mugire</h2>
				<p class="text-base leading-relaxed text-muted-foreground sm:text-lg">
					Working primarily with raw pigments, acrylic polymers, and natural fibers, David explores
					how physical depth creates quiet points of focus in architectural spaces.
				</p>
				<div>
					<Button href="/about" variant="outline" color='secondary' class="mt-2">Read Full Profile</Button>
				</div>
			</div>
		</div>
	</section>
</div>

<!-- ==========================================
     E. FEATURED WORKS — scrub-in grid + magnetic tilt
     ========================================== -->
<section class="px-4 py-24 sm:px-8 lg:px-16">
	<div class="mx-auto max-w-7xl">
		<div
			class="mb-12 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-end"
			use:animate={{
				type: 'from',
				opacity: 0,
				y: 40,
				ease: 'none',
				scrollTrigger: {
					start: 'top 95%',
					end: 'top 65%',
					scrub: true
				}
			}}
		>
			<div>
				<p class="mb-2 text-xs font-bold tracking-[0.2em] uppercase text-muted-foreground">
					Selected Originals
				</p>
				<h2 class="font-display text-3xl font-bold sm:text-5xl">Recent Studio Works</h2>
			</div>
			<Button href="/catalog" variant="outline" color='secondary'>View All Works</Button>
		</div>

		{#if featuredWork.length > 0}
			<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
				{#each featuredWork as item, i (item.catalog_id)}
					<a
						href="/catalog/{item.catalog_id}"
						class="group flex flex-col gap-3 [transform-style:preserve-3d] will-change-transform"
						onmousemove={tiltCard}
						onmouseleave={resetCard}
						use:animate={{
							type: 'from',
							opacity: 0,
							y: 90,
							scale: 0.85,
							rotate: i % 2 === 0 ? -6 : 6,
							ease: 'none',
							scrollTrigger: {
								start: `top ${95 - (i % 4) * 4}%`,
								end: `top ${55 - (i % 4) * 4}%`,
								scrub: true
							}
						}}
					>
						<div class="relative aspect-[3/4] w-full overflow-hidden rounded-md bg-muted">
							<img
								src={`${PUBLIC_BACKEND_URL}/${item.image}`}
								alt={item.name}
								class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
							/>
						</div>
						<div class="flex items-baseline justify-between pt-2">
							<h3 class="font-display text-base font-semibold">{item.name}</h3>
							<span class="text-xs font-mono text-muted-foreground">
								#{String(i + 1).padStart(2, '0')}
							</span>
						</div>
						<p class="text-xs text-muted-foreground">{item.category ?? 'Original Artwork'}</p>
					</a>
				{/each}
			</div>
		{:else}
			<p class="py-12 text-center text-muted-foreground">No featured works available at present.</p>
		{/if}
	</div>
</section>

<!-- ==========================================
     G. NEWSLETTER & CTA — scrub scale-in
     ========================================== -->
<section class="px-4 py-16 sm:px-8 lg:px-16 bg-foreground">
	<div
		class="mx-auto max-w-7xl rounded-2xl bg-foreground p-8 text-background sm:p-16"
		use:animate={{
			type: 'from',
			scale: 0.85,
			opacity: 0,
			ease: 'none',
			scrollTrigger: {
				start: 'top 95%',
				end: 'top 55%',
				scrub: true
			}
		}}
	>
		<div class="grid grid-cols-1 gap-8 lg:grid-cols-12 lg:items-center">
			<div class="lg:col-span-7">
				<h2 class="font-display text-3xl font-bold leading-tight sm:text-5xl">
					Join the Private Studio List
				</h2>
				<p class="mt-4 text-sm text-background/70 sm:text-base">
					Get early notifications before new collections drop and private availability for
					commissions.
				</p>
			</div>
			<div class="lg:col-span-5">
				<form class="flex flex-col gap-3 sm:flex-row" onsubmit={(e) => e.preventDefault()}>
					<Input type="email" placeholder="Enter your email" context="dark" />
					<Button
						type="submit"
						variant="filled"
						color='white'
					>
						Subscribe
					</Button>
				</form>
			</div>
		</div>
	</div>
</section>
