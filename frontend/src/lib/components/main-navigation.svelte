<script lang="ts">
	import { page } from '$app/state';
	import MainNavLinks, { navLinks } from './main-nav-links.svelte';
	import Button from './ui/button/button.svelte';
	import Menu from '@tabler/icons-svelte-runes/icons/menu';
	import X from '@tabler/icons-svelte-runes/icons/x';
	import { slide, fade, fly } from 'svelte/transition';
	import { backOut, cubicOut } from 'svelte/easing';

	let isOpen = $state(false);

	function toggleMenu() {
		isOpen = !isOpen;
	}

	function closeMenu() {
		isOpen = false;
	}

	const isActive = (href: string) => page.url.pathname === href;
</script>

<!-- Backdrop overlay -->
{#if isOpen}
	<div
		transition:fade={{ duration: 200 }}
		onclick={closeMenu}
		onkeydown={(e) => e.key === 'Escape' && closeMenu()}
		role="button"
		tabindex="-1"
		aria-label="Close navigation overlay"
		class="fixed inset-0 bg-black/80 backdrop-blur-lg z-40 md:hidden"
	></div>
{/if}

<nav
	class="bg-surface/80 sm:bg-background/80 z-[50] border-b border-surface-border/50 shadow-lg w-full lg:w-[65%] rounded-none md:lg:rounded-full transition-all duration-300 relative isolate"
>
	<!-- Main Header Bar -->
	<div class="h-15 flex items-center justify-between pr-4 pl-8 relative z-10">
		<div>
			<a
				href="/"
				onclick={closeMenu}
				class="font-light text-foreground font-display text-xl tracking-wide"
			>
				Studio Mugire
			</a>
		</div>

		<!-- Desktop Navigation -->
		<div class="hidden md:block absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
			<MainNavLinks />
		</div>

		<!-- Action Controls -->
		<div class="flex items-center gap-2">
			<!-- Mobile Toggle Button -->
			<Button
				size="icon"
				variant="filled"
				color="black"
				onclick={toggleMenu}
				aria-expanded={isOpen}
				aria-label="Toggle Navigation Menu"
				class="md:hidden relative overflow-hidden transition-transform duration-300 active:scale-90"
			>
				<div
					class="transition-transform duration-300 flex items-center justify-center"
					style="transform: rotate({isOpen ? '90deg' : '0deg'})"
				>
					{#if isOpen}
						<X class="size-5" />
					{:else}
						<Menu class="size-5" />
					{/if}
				</div>
			</Button>

			<!-- Desktop CTA -->
			<Button
				href="/classes"
				variant={isActive('/classes') ? 'filled' : 'outline'}
				color="black"
				class="hidden md:flex"
			>
				Book a class
			</Button>
		</div>
	</div>

	<!-- Playful Mobile Drawer -->
	{#if isOpen}
		<div
			transition:slide={{ duration: 350, easing: cubicOut }}
			class="md:hidden border-t border-white/10 overflow-hidden bg-transparent rounded-b-3xl"
		>
			<div class="px-6 pt-6 pb-8 flex flex-col items-center gap-6 text-center">
				<!-- Individual Mobile Nav Links with Staggered Entrance -->
				<ul class="w-full flex flex-col items-center space-y-2">
					{#each navLinks as link, index (link.name)}
						<li
							in:fly={{ y: 20, duration: 300, delay: 80 + index * 50, easing: backOut }}
							class="w-full text-left"
						>
							<a
								href={link.href}
								onclick={closeMenu}
								class={`block py-2.5 px-4 rounded-full text-base font-medium transition-all duration-200 ${
									isActive(link.href)
										? 'bg-black text-white font-semibold'
										: 'text-foreground/80 hover:text-white hover:bg-background'
								}`}
							>
								{link.name}
							</a>
						</li>
					{/each}
				</ul>

				<!-- Divider -->
				<div
					in:fly={{ y: 15, duration: 250, delay: 80 + navLinks.length * 50 }}
					class="w-12 h-0.5 bg-white/20 rounded-full"
				></div>

				<!-- Mobile CTA Button -->
				<div
					in:fly={{ y: 20, duration: 300, delay: 120 + navLinks.length * 50, easing: backOut }}
					class="w-full max-w-xs"
				>
					<Button
						href="/classes"
						variant={isActive('/classes') ? 'filled' : 'outline'}
						color="black"
						onclick={closeMenu}
						class="w-full py-3 text-base shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-transform"
					>
						Book a class
					</Button>
				</div>
			</div>
		</div>
	{/if}
</nav>

<style>
	nav {
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
	}
</style>
