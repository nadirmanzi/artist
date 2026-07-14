<script lang="ts">
	import Menu from '@tabler/icons-svelte-runes/icons/menu';
	import MainNavLinks from './main-nav-links.svelte';
	import Button from './ui/button/button.svelte';
	import { page } from '$app/state';

</script>

<nav
	class="bg-foreground/50 z-[999] backdrop-blur-md border border-black/20 text-foreground h-15 lg:rounded-full lg:w-[65%] w-full flex items-center justify-between pr-4 pl-8"
>
	<div class="">
		<p class="font-light text-white font-display text-xl">Studio Mugire</p>
	</div>

	<div class="hidden md:block absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
		<MainNavLinks />
	</div>

	<div class="">
		<div class="">
			<Button size="icon" variant="outline" color="white" class="md:hidden"><Menu /></Button>
		</div>

		<div class="">
			<Button
				href="/classes"
				variant={page.url.pathname === '/classes' ? 'filled' : 'outline'}
				color="white"
				class="hidden md:block">Book a class</Button
			>
		</div>
	</div>
</nav>
