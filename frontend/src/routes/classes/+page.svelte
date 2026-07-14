<script lang="ts">
	import PageBanner from '$lib/components/page-banner.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import BrandWhatsappFilled from '@tabler/icons-svelte-runes/icons/brand-whatsapp-filled';
	import InfoCircle from '@tabler/icons-svelte-runes/icons/info-circle';

	const lessons = $state([
		{
			name: 'Intro to Oil Painting',
			description: 'Master the basics of color mixing, brushwork, and layering with oil mediums.',
			max_students: 12,
			hours_per_session: 3,
			total_sessions: 6,
			price: 240
		},
		{
			name: 'Mixed Media Mashup',
			description: 'Combine acrylics, collage, and ink to create textured, modern art pieces.',
			max_students: 10,
			hours_per_session: 2.5,
			total_sessions: 4,
			price: 180
		},
		{
			name: 'Advanced Portraiture',
			description:
				'Capture human expression and anatomy using advanced shading and structural drawing techniques.',
			max_students: 8,
			hours_per_session: 3,
			total_sessions: 8,
			price: 350
		},
		{
			name: 'Watercolor Landscapes',
			description: 'Learn to control washes, transparency, and light to paint outdoor scenery.',
			max_students: 15,
			hours_per_session: 2,
			total_sessions: 5,
			price: 150
		},
		{
			name: 'Palette Knife Techniques',
			description:
				'Ditch the brushes and build heavy texture using acrylic paints and painting knives.',
			max_students: 10,
			hours_per_session: 2,
			total_sessions: 3,
			price: 125
		},
		{
			name: 'Clay Sculpting Basics',
			description: 'An introduction to hand-building techniques, form, and basic glazing.',
			max_students: 8,
			hours_per_session: 3,
			total_sessions: 6,
			price: 280
		}
	]);
</script>

<PageBanner text="Lean to paint. Learn to see." image="/art-1.jpeg" />

<div class="flex items-center justify-center space-x-2 py-10">
	<div class="">
		<InfoCircle class="text-white size-8 fill-primary" />
	</div>

	<div class="flex items-center space-x-2">
		<p class="font-bold">Note:</p>
		<p>All booking confirmations and future inquiries are handled via</p>

		<p class="text-[#25d366] flex items-center space-x-1">
			<BrandWhatsappFilled /> <span>Whatsapp</span>
		</p>
	</div>
</div>

<div class="grid grid-cols-3 p-20 gap-0 bg-surface">
	{#each lessons as lesson, index (lesson.name)}
		<div class={` p-8 ${index % 3 === 1 ? 'border-x' : ''} border-b border-black/20 space-y-8`}>
			<div class="space-y-2">
				<p
					class="font-display font-semibold text-2xl underline underline-offset-8 decoration-solid"
				>
					{lesson.name}
				</p>
			</div>

			<div class="">
				<p class="text-surface-foreground-muted">{lesson.description}</p>
			</div>

			<Button class=" w-full mt-10" color="black" variant="tonal">Book Now</Button>
		</div>
	{/each}
</div>
