<script lang="ts">
	import ArtistImage from '$lib/assets/artist.jpeg';
	import { Button } from '$lib/components/ui/button';
	import PageBanner from '$lib/components/page-banner.svelte';
	import { animate } from '$lib/utils/animate';
	import { gsap } from 'gsap';

	// Playful hover tilt for the practice cards (section 03) — cursor-driven, additive only.
	function tiltCard(e: MouseEvent) {
		const card = e.currentTarget as HTMLElement;
		const rect = card.getBoundingClientRect();
		const px = (e.clientX - rect.left) / rect.width;
		const py = (e.clientY - rect.top) / rect.height;

		gsap.to(card, {
			rotateX: (py - 0.5) * -8,
			rotateY: (px - 0.5) * 8,
			y: -4,
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
				y: 0,
				duration: 0.6,
				ease: 'power3.out'
			} as gsap.TweenVars
		);
	}
</script>

<svelte:head>
	<title>Meet the Artist</title>
</svelte:head>

<PageBanner text="Where painting becomes a conversation with the world." image="/art-2.jpeg" />

<!-- SECTION 01: THE STUDIO -->
<div
	class="px-6 sm:px-10 pt-12 md:pt-20 pb-16 md:pb-30 grid grid-cols-1 lg:grid-cols-2 gap-10 border-b bg-surface border-black/20"
>
	<div
		class="h-[50dvh] sm:h-[60dvh] lg:h-[80dvh] w-full flex items-center justify-center overflow-hidden"
	>
		<img src="/images/studio.jpg" alt="The Studio" class="h-full w-full lg:w-[80%] object-cover" />
	</div>

	<div
		class="space-y-4 px-0 lg:px-10 flex flex-col justify-center"
		use:animate={{
			type: 'from',
			opacity: 0,
			y: 70,
			ease: 'none',
			scrollTrigger: {
				start: 'top 70%',
				end: 'top 0%',
				scrub: true
			}
		}}
	>
		<p
			class="text-surface-foreground-muted text-sm"
			use:animate={{
				type: 'from',
				opacity: 0,
				x: -20,
				ease: 'none',
				scrollTrigger: {
					start: 'top 100%',
					end: 'top 90%',
					scrub: true
				}
			}}
		>
			01 / The Studio
		</p>

		<p class="font-display font-semibold text-3xl sm:text-4xl">Studio Mugire</p>

		<div class="space-y-6 py-8 border-b border-black/30 text-surface-foreground-muted">
			<p>
				Studio Mugire is a contemporary art studio and gallery based in Kigali, Rwanda. Founded as a
				space where art making and reflection converge, the studio produces original works across
				painting, mixed media, and commissions.
			</p>

			<p>
				The name Mugire — meaning "let it grow" in Kinyarwanda — captures the studio's ethos: a
				commitment to organic creative development, rooted in place and open to the world.
			</p>

			<p>
				The studio welcomes collectors, institutions, and individuals seeking original artworks,
				custom commissions, and immersive workshops led by the artist.
			</p>
		</div>

		<div class="grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-4 py-6">
			{#each [{ label: 'Practice', value: 'Painting & Mixed Media' }, { label: 'Location', value: 'Kigali, Rwanda' }, { label: 'Founded', value: '2018' }] as stat, i (stat.label)}
				<div
					class="flex flex-col space-y-2 sm:space-y-4"
					use:animate={{
						type: 'from',
						opacity: 0,
						y: 30,
						scale: 0.9,
						ease: 'none',
						scrollTrigger: {
							start: `top ${95 - i * 4}%`,
							end: `top ${65 - i * 4}%`,
							scrub: true
						}
					}}
				>
					<p class="text-surface-foreground-muted">{stat.label}</p>
					<p class="font-medium">{stat.value}</p>
				</div>
			{/each}
		</div>
	</div>
</div>

<!-- SECTION 02: THE ARTIST -->
<div
	class="px-6 sm:px-10 pt-12 md:pt-20 pb-16 md:pb-30 grid grid-cols-1 lg:grid-cols-2 gap-10 border-b bg-surface border-black/10"
>
	<div
		class="space-y-4 px-0 lg:px-10 flex flex-col justify-center order-2 lg:order-1"
		use:animate={{
			type: 'from',
			opacity: 0,
			x: -70,
			ease: 'none',
			scrollTrigger: {
				start: 'top 100%',
				end: 'top 90%',
				scrub: true
			}
		}}
	>
		<p class="text-surface-foreground-muted text-sm">02 / The Artist</p>

		<p class="font-display font-semibold text-3xl sm:text-4xl">Mugire Peace David</p>

		<div class="space-y-6 py-8 border-b border-black/30 text-surface-foreground-muted">
			<p>
				Mugire Peace David is a Rwandan contemporary artist whose practice spans painting, mixed
				media, and site-specific installations. His work draws on landscape, memory, and the
				textures of everyday life in Central Africa, rendered through layered surfaces and
				restrained palettes.
			</p>

			<p>
				Trained in fine arts and self-developed through years of rigorous studio practice, David's
				work has been exhibited across Rwanda and internationally. Each canvas is an act of
				listening — to place, to material, to the quiet forces that shape a life.
			</p>

			<p>
				Beyond the canvas, he facilitates workshops and classes designed to bring people into
				contact with their own creative instincts, fostering a broader culture of making in Kigali
				and beyond.
			</p>
		</div>

		<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 py-6 gap-3 sm:gap-4">
			{#each ['Painting', 'Mixed Media', 'Landscapes', 'Commissions', 'Workshops'] as tag, i (tag)}
				<div
					class={`border text-center p-2 rounded-lg border-black/20 transition-transform duration-200 hover:-translate-y-1 hover:rotate-1 hover:border-black/40 ${i === 4 ? 'col-span-2 sm:col-span-1' : ''}`}
					use:animate={{
						type: 'from',
						opacity: 0,
						scale: 0.5,
						rotate: i % 2 === 0 ? -10 : 10,
						ease: 'back.out(2.5)',
						scrollTrigger: {
							start: `top ${92 - i * 3}%`,
							end: `top ${68 - i * 3}%`,
							scrub: true
						}
					}}
				>
					<p class="text-surface-foreground-muted text-sm">{tag}</p>
				</div>
			{/each}
		</div>
	</div>

	<div
		class="h-[50dvh] sm:h-[60dvh] lg:h-[80dvh] w-full flex items-center justify-center order-1 lg:order-2 overflow-hidden"
	>
		<img src={ArtistImage} alt="Mugire Peace David" class="h-full w-full lg:w-[80%] object-cover" />
	</div>
</div>

<!-- SECTION 03: PRACTICE -->
<div class="px-6 sm:px-10 pt-12 md:pt-20 pb-16 md:pb-30 flex flex-col gap-10">
	<div
		class="space-y-4 px-0 lg:px-10 flex flex-col justify-center"
		use:animate={{
			type: 'from',
			opacity: 0,
			y: 40,
			ease: 'none',
			scrollTrigger: {
				start: 'top 95%',
				end: 'top 70%',
				scrub: true
			}
		}}
	>
		<p class="text-surface-foreground-muted">03 / Practice</p>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-3 rounded-lg overflow-hidden gap-8 md:gap-0">
		{#each [{ title: 'Original Artworks', copy: 'A growing body of original paintings and mixed media works available for acquisition. Each piece is unique, produced in the studio with intention and care.' }, { title: 'Commissions', copy: 'Custom works created in close collaboration with collectors and institutions. The artist works from references, conversations, and site visits to produce pieces made for specific spaces and people.' }, { title: 'Workshops & Classes', copy: 'Studio sessions open to individuals and groups — from beginners to practicing artists. The workshops explore painting, mixed media, and creative process in an intimate studio environment.' }] as practice, i (practice.title)}
			<div
            role='button'
            tabindex='0'
				class={`relative px-0 md:px-10 py-4 md:py-4 space-y-6 md:space-y-8 transform-3d will-change-transform ${
					i === 1 ? 'border-y md:border-y-0 md:border-x border-black/20 py-8' : ''
				}`}
				onmousemove={tiltCard}
				onmouseleave={resetCard}
			>
				<!-- Accent line draws in per-card, staggered like a row of dominoes -->
				<div
					class="absolute left-0 md:left-10 top-0 h-0.5 w-[calc(100%)] md:w-[calc(100%-5rem)] origin-left bg-foreground/70"
					use:animate={{
						type: 'from',
						scaleX: 0,
						ease: 'none',
						scrollTrigger: {
							start: `top ${95 - i * 5}%`,
							end: `top ${70 - i * 5}%`,
							scrub: true
						}
					}}
				></div>

				<div
					use:animate={{
						type: 'from',
						opacity: 0,
						y: 50,
						scale: 0.94,
						ease: 'none',
						scrollTrigger: {
							start: `top ${95 - i * 5}%`,
							end: `top ${60 - i * 5}%`,
							scrub: true
						}
					}}
				>
					<div class="space-y-2">
						<p class="font-display text-2xl sm:text-3xl">{practice.title}</p>
					</div>
					<p class="text-surface-foreground-muted">{practice.copy}</p>
				</div>
			</div>
		{/each}
	</div>
</div>

<!-- CTA SECTION -->

<div class="bg-foreground">
	<div
		class="px-6 sm:px-10 py-12 md:py-20 bg-foreground text-white"
		use:animate={{
			type: 'from',
			opacity: 0.5,
			scale: 0.9,
			rotate: -1,
			ease: 'none',
			scrollTrigger: {
				start: 'top 95%',
				end: 'top 55%',
				scrub: true
			}
		}}
	>
		<div
			class="flex flex-col lg:flex-row items-start lg:items-center justify-between lg:justify-evenly gap-8 lg:gap-0"
		>
			<div class="space-y-4 md:space-y-6">
				<p class="text-2xl sm:text-3xl md:text-4xl font-display font-semibold">
					Interested in working together?
				</p>
				<p class="text-nav-foreground-muted">
					Reach out to discuss commissions, classes, or studio visits
				</p>
			</div>

			<div class="flex flex-col sm:flex-row w-full lg:w-auto gap-3 sm:space-x-2">
				<Button
					class="w-full sm:w-auto transition-transform duration-300 hover:scale-105 hover:-rotate-1"
					color="white"
					size="lg"
					href="/contacts"
				>
					Get in Touch
				</Button>
				<Button
					class="w-full sm:w-auto transition-transform duration-300 hover:scale-105 hover:rotate-1"
					color="white"
					size="lg"
					variant="outline"
					href="/catalog"
				>
					View Catalog
				</Button>
			</div>
		</div>
	</div>
</div>
