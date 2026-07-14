<script>
	import AnimatedPillGroup from './ui/animated-pill/animated-pill-group.svelte';
	import AnimatedPillItem from './ui/animated-pill/animated-pill-item.svelte';
	import { page } from '$app/state';

	const navLinks = [
		{ name: 'Home', href: '/' },
		{ name: 'Catalog', href: '/catalog' },
		{ name: 'About', href: '/about' },
		{ name: 'Contacts', href: '/contacts' }
	];

	const activeLink = (link) => {
		return page.url.pathname === link.href;
	};
</script>

<div class="">
	<AnimatedPillGroup class="flex items-center space-x-0" direction="horizontal" color="white">
		{#each navLinks as link (link.name)}
				<AnimatedPillItem
					active={activeLink(link)}
					href={link.href}
					
					class={`${activeLink(link) ? 'text-foreground font-semibold text-sm' : 'text-white/80 hover:text-foreground'} ${link.href === '/' ? 'opacity-50 cursor-not-allowed pointer-events-none' : ''} px-4 text-sm py-2`}
				>
					{link.name}
				</AnimatedPillItem>
		{/each}
	</AnimatedPillGroup>
</div>
