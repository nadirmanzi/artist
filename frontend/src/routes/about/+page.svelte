<script lang="ts">
	import ArtistImage from '$lib/assets/artist.jpeg';
	import StudioImage from '$lib/assets/studio.jpeg';
	import { Button } from '$lib/components/ui/button';
	import PageBanner from '$lib/components/page-banner.svelte';
	import { animate } from '$lib/utils/animate';
</script>

<svelte:head>
	<title>Meet the Artist</title>
</svelte:head>

<PageBanner
	text="Exploring the connection between nature, color, and emotion"
	image="/images/about-banner.PNG"
/>

<!-- SECTION 01: THE STUDIO -->
<div
	class="px-6 sm:px-10 pt-12 md:pt-20 pb-16 md:pb-30 grid grid-cols-1 lg:grid-cols-2 gap-10 border-b bg-surface border-black/20"
>
	<div
		class="h-[50dvh] sm:h-[60dvh] lg:h-[80dvh] w-full flex items-center justify-center overflow-hidden"
	>
		<img src={StudioImage} alt="The Studio" class="h-full w-full lg:w-[80%] object-cover rounded-3xl" />
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

		<div class="space-y-6 py-8 border-b border-black/30 text-foreground">
			<p>
				Studio Mugire is a contemporary art studio and gallery based in Kigali, Rwanda, founded by
				artist David Mugire. The studio brings together original artworks, exhibitions, creative
				experiences, and opportunities for people to engage with art in different ways.
			</p>

			<p>
				Inspired by nature and the emotions found within it, Studio Mugire explores the relationship
				between color, texture, and imagination. Through paintings, workshops, collaborations, and
				conversations, the studio creates a space where people can discover, experience, and connect
				with contemporary art.
			</p>

			<p>
				We welcome you to visit Studio Mugire and experience a place where creativity, stories, and
				nature meet.
			</p>
		</div>

		<div class="grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-4 py-6">
			{#each [{ label: 'Practice', value: 'Landscape Paintings & Mixed Media' }, { label: 'Location', value: 'Kigali, Rwanda' }, { label: 'Founded', value: '2022' }] as stat, i (stat.label)}
				<div
					class="flex flex-col space-y-2 sm:space-y-4 text-right"
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
					<p class="text-secondary font-semibold">{stat.label}</p>
					<p class="">{stat.value}</p>
				</div>
			{/each}
		</div>
	</div>
</div>

<!-- SECTION 02: THE ARTIST -->
<div
	class="px-6 sm:px-10 pt-12 md:pt-20 pb-16 md:pb-10 grid grid-cols-1 lg:grid-cols-2 gap-10 border-b bg-surface border-black/10"
>
	<div class="space-y-4 px-0 lg:px-10 flex flex-col justify-center order-2 lg:order-1">
		<!-- Header / Subtitle -->
		<p
			class="text-surface-foreground-muted text-sm"
			use:animate={{
				type: 'from',
				opacity: 0,
				x: -20,
				ease: 'none',
				scrollTrigger: {
					start: 'top 95%',
					end: 'top 85%',
					scrub: true
				}
			}}
		>
			02 / The Artist
		</p>

		<p
			class="font-display font-semibold text-3xl sm:text-4xl"
			use:animate={{
				type: 'from',
				opacity: 0,
				y: 30,
				ease: 'none',
				scrollTrigger: {
					start: 'top 90%',
					end: 'top 80%',
					scrub: true
				}
			}}
		>
			Mugire Peace David
		</p>

		<div class="space-y-6 py-8 text-foreground">
			<!-- Block 1: The Journey -->
			<div
				class="space-y-4 border-b border-surface-border py-4"
				use:animate={{
					type: 'from',
					opacity: 0,
					y: 40,
					ease: 'none',
					scrollTrigger: {
						start: 'top 85%',
						end: 'top 65%',
						scrub: true
					}
				}}
			>
				<p class="text-secondary font-semibold font-display">The Journey</p>
				<p>
					Born and based in Rwanda, David Mugire developed a deep connection with art through his
					fascination with the landscapes, colors, and stories that surround him. His artistic
					journey led him to study at Nyundo School of Arts, where he continued developing his
					creative language and exploring different approaches to painting. Over the years, his
					practice has evolved into a distinctive style centered around texture, movement, and the
					emotional power of landscapes.
				</p>
			</div>

			<!-- Block 2: Artistic Practice -->
			<div
				class="space-y-4 border-b border-surface-border py-4"
				use:animate={{
					type: 'from',
					opacity: 0,
					y: 40,
					ease: 'none',
					scrollTrigger: {
						start: 'top 80%',
						end: 'top 60%',
						scrub: true
					}
				}}
			>
				<p class="text-secondary font-semibold font-display">Artistic Practice</p>
				<p>
					Working primarily with palette knives and mixed media techniques, David creates richly
					textured surfaces where layers of color and materials build depth, movement, and emotion.
					His landscapes are not simply representations of places, but reflections of feelings,
					memories, and personal experiences. Through each layer, he explores the connection between
					people and the natural world, inviting viewers to experience landscapes beyond what is
					visible.
				</p>
			</div>

			<!-- Block 3: Inspiration & Themes -->
			<div
				class="space-y-4 border-b border-surface-border py-4"
				use:animate={{
					type: 'from',
					opacity: 0,
					y: 40,
					ease: 'none',
					scrollTrigger: {
						start: 'top 75%',
						end: 'top 55%',
						scrub: true
					}
				}}
			>
				<p class="font-semibold font-display text-secondary">Inspiration & Themes</p>

				<div class="space-y-2">
					<p>
						Nature is at the heart of David’s practice. Through landscapes, he explores moments of
						peace, reflection, and the quiet beauty found in the world around us.
					</p>

					<p>
						Texture allows David to create a deeper relationship between the artwork and the viewer.
						Each layer carries movement, energy, and emotion, transforming the surface into an
						experience.
					</p>
				</div>
			</div>

			<!-- Block 4: Selected Exhibitions -->
			<div
				class="space-y-4 py-4"
				use:animate={{
					type: 'from',
					opacity: 0,
					y: 40,
					ease: 'none',
					scrollTrigger: {
						start: 'top 70%',
						end: 'top 50%',
						scrub: true
					}
				}}
			>
				<p class="font-semibold text-secondary font-display">Selected Exhibitions</p>

				<ul class="space-y-2 list-disc px-4">
					<li>Talk Melanin - Art Fair Brussels, Belgium (2026)</li>
					<li>Rwanda Nziza – Try Out Art Gallery, Belgium (2024)</li>
					<li>Standing on a Thousand Hills – Mechelen, Belgium (2024)</li>
					<li>Africanism – L’ESPACE, Kigali (2021)</li>
					<li>Mama Rwanda (2019)</li>
				</ul>
			</div>
		</div>
	</div>

	<div
		class="h-[50dvh] sm:h-[60dvh] sm:sticky sm:top-24 lg:h-[80dvh] w-full flex items-center justify-center order-1 lg:order-2 overflow-hidden"
	>
		<img src={ArtistImage} alt="Mugire Peace David" class="h-full w-full lg:w-[80%] object-cover rounded-3xl" />
	</div>
</div>

<!-- SECTION 03: PRACTICE -->
<div class="px-6 sm:px-10 pt-12 md:pt-20 pb-16 md:pb-30 flex flex-col gap-10 bg-background">
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
		<p class="text-surface-foreground-muted">03 / More</p>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-3 rounded-lg overflow-hidden gap-8 md:gap-0">
		{#each [{ title: 'Projects', copy: 'David Mugire’s work extends beyond the studio through projects in hospitality, literature, community engagement, and international cultural initiatives, including SINGITA KWITONDA LODGE, UNESCO Headquarters in Paris, Jacaranda by GAËL FAYE, and UNHCR Rwanda.' }, { title: 'Collaborations', copy: 'At Studio Mugire, we believe collaboration creates meaningful connections between art, people, and ideas. We welcome partnerships with galleries, cultural institutions, hospitality brands, designers, schools, and organizations.' }, { title: 'Artist Talks & Lectures', copy: 'David Mugire has been invited to share his artistic journey through talks and lectures at ACADÉMIE MECHELEN, ACADÉMIE POPERINGE, and GREEN HILLS ACADEMY, inspiring conversations around art, creativity, and contemporary practice.' }] as practice, i (practice.title)}
			<div
				role="button"
				tabindex="0"
				class={`relative px-0 md:px-10 py-4 md:py-4 space-y-6 md:space-y-8 ${
					i === 1 ? 'border-y md:border-y-0 md:border-x border-black/20 py-8' : ''
				}`}
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
							end: `top ${75 - i * 5}%`,
							scrub: true
						}
					}}
				>
					<div class="space-y-4">
						<p class="font-display text-2xl sm:text-3xl">{practice.title}</p>
						<p class="text-surface-foreground-muted">{practice.copy}</p>
					</div>
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
				end: 'top 60%',
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
