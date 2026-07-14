<script lang="ts">
	import StudioImage from '$lib/assets/studio.jpg';
	import ArtistImage from '$lib/assets/artist.jpeg';
	import { Button } from '$lib/components/ui/button';
	import PageBanner from '$lib/components/page-banner.svelte';
</script>

<svelte:head>
	<title>Meet the Artist</title>
</svelte:head>

<PageBanner text='Where painting becomes a conversation with the world.' image='/art-2.jpeg' />

<div class="px-10 pt-20 pb-30 grid grid-cols-2 gap-10 border-b bg-surface border-black/20">
	<div class="h-[80dvh] w-full flex items-center justify-center">
		<img src={StudioImage} alt="" class="h-full w-[80%] object-cover" />
	</div>

	<div class="space-y-4 px-10 flex flex-col justify-center">
		<p class="text-surface-foreground-muted text-sm">01 / The Studio</p>

		<p class="font-display font-semibold text-4xl">Studio Mugire</p>

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

		<div class="grid grid-cols-3 py-6">
			<div class="flex flex-col space-y-4">
				<p class="text-surface-foreground-muted">Practice</p>
				<p class="font-medium">Painting & Mixed Media</p>
			</div>

			<div class="flex flex-col space-y-4">
				<p class="text-surface-foreground-muted">Location</p>
				<p class="font-medium">Kigali, Rwanda</p>
			</div>

			<div class="flex flex-col space-y-4">
				<p class="text-surface-foreground-muted">Founded</p>
				<p class="font-medium">2018</p>
			</div>
		</div>
	</div>
</div>

<div class="px-10 pt-20 pb-30 grid grid-cols-2 gap-10 border-b bg-surface border-black/10">
	<div class="space-y-4 px-10 flex flex-col justify-center">
		<p class="text-surface-foreground-muted text-sm">02 / The Artist</p>

		<p class="font-display font-semibold text-4xl">Mugire Peace David</p>

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

		<div class="grid grid-cols-5 py-6 gap-4">
			<div class="border text-center p-2 rounded-lg border-black/20">
				<p class="text-surface-foreground-muted">Painting</p>
			</div>

			<div class="border text-center p-2 rounded-lg border-black/20">
				<p class="text-surface-foreground-muted">Mixed Media</p>
			</div>

			<div class="border text-center p-2 rounded-lg border-black/20">
				<p class="text-surface-foreground-muted">Landscapes</p>
			</div>

			<div class="border text-center p-2 rounded-lg border-black/20">
				<p class="text-surface-foreground-muted">Commissions</p>
			</div>

			<div class="border text-center p-2 rounded-lg border-black/20">
				<p class="text-surface-foreground-muted">Workshops</p>
			</div>
		</div>
	</div>

	<div class="h-[80dvh] w-full flex items-center justify-center">
		<img src={ArtistImage} alt="" class="h-full w-[80%] object-cover" />
	</div>
</div>

<div class="px-10 pt-20 pb-30 flex flex-col gap-10">
	<div class="space-y-4 px-10 flex flex-col justify-center">
		<p class="text-surface-foreground-muted">03 / Practice</p>
	</div>

	<div class="grid grid-cols-3 rounded-lg overflow-hidden">
		<div class="px-10 py-4 space-y-8">
			<div class="space-y-2">
				<p class=" font-display text-3xl">Original Artworks</p>
			</div>
			<p class="text-surface-foreground-muted">
				A growing body of original paintings and mixed media works available for acquisition. Each
				piece is unique, produced in the studio with intention and care.
			</p>
		</div>

		<div class="border-x px-10 py-4 border-black/20 space-y-8">
			<div class="space-y-2">
				<p class=" font-display text-3xl">Commissions</p>
			</div>
			<p class="text-surface-foreground-muted">
				Custom works created in close collaboration with collectors and institutions. The artist
				works from references, conversations, and site visits to produce pieces made for specific
				spaces and people.
			</p>
		</div>

		<div class="px-10 py-4 space-y-8">
			<div class="space-y-2">
				<p class=" font-display text-3xl">Workshops & Classes</p>
			</div>
			<p class="text-surface-foreground-muted">
				Studio sessions open to individuals and groups — from beginners to practicing artists. The
				workshops explore painting, mixed media, and creative process in an intimate studio
				environment.
			</p>
		</div>
	</div>
</div>

<div class="px-10 pt-20 pb-30 bg-foreground text-white">
	<div class="flex items-center justify-evenly">
		<div class="space-y-6">
			<p class="text-4xl font-display font-semibold">Interested in working together?</p>
			<p class="text-nav-foreground-muted">
				Reach out to discuss commissions, classes, or studio visits
			</p>
		</div>

		<div class="flex scroll-px-6 justify-end space-x-2">
			<Button class="" color="white" size="lg" href='/contacts'>Get in Touch</Button>
			<Button class="" color="white" size="lg" variant="outline" href='/catalog'>View Catalog</Button>
		</div>
	</div>
</div>
