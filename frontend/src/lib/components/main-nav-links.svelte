<script module>
	export const navLinks = [
		{ name: 'Home', href: '/' },
		{ name: 'Catalog', href: '/catalog' },
		{ name: 'About', href: '/about' },
		{ name: 'Contacts', href: '/contacts' }
	];
</script>

<script lang="ts">
	import AnimatedPillGroup from './ui/animated-pill/animated-pill-group.svelte';
	import AnimatedPillItem from './ui/animated-pill/animated-pill-item.svelte';
	import { page } from '$app/state';

	const activeLink = (link: { href: string }) => {
		return page.url.pathname === link.href;
	};
</script>

<div class="">
	<AnimatedPillGroup
		class="flex items-center space-x-0"
		direction="horizontal"
		color="var(--color-primary)"
	>
		{#each navLinks as link (link.name)}
			<AnimatedPillItem
				active={activeLink(link)}
				href={link.href}
				class={`${activeLink(link) ? 'text-foreground font-semibold text-sm' : 'text-white font-medium hover:text-foreground'} px-4 text-sm py-2`}
			>
				{link.name}
			</AnimatedPillItem>
		{/each}
	</AnimatedPillGroup>
</div>
