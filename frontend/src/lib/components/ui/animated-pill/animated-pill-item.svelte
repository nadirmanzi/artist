<script lang="ts">
	/*
	 * ─── ANIMATED PILL ITEM ────────────────────────────────────────────────────
	 * A lightweight wrapper that attaches its children to the nearest Pill Group.
	 * Highly unopinionated: provides a `data-active` attribute for custom styling.
	 * ───────────────────────────────────────────────────────────────────────────────
	 */
	import { cn } from '$lib/utils';
	import type { Snippet } from 'svelte';
	import { getPillGroup } from './animated-pill-group.svelte';

	interface Props {
		/** Forcefully toggle the group's "active" state to this item */
		active?: boolean;
		href?: string;
		children: Snippet;
		class?: string;
		onclick?: (e: MouseEvent) => void;
		onmouseenter?: (e: MouseEvent) => void;
		onmouseleave?: (e: MouseEvent) => void;
	}

	let {
		active = false,
		href,
		children,
		class: className,
		onclick,
		onmouseenter,
		onmouseleave
	}: Props = $props();

	const group = getPillGroup();
	const pillTracker = group?.pillTracker;

	// Optional fallback if used outside of a group
	function fallbackAction(node: HTMLElement) {
		return {};
	}
	const action = pillTracker || fallbackAction;
</script>

{#if href}
	<a
		use:action={{ active }}
		{href}
		class={cn(
			'flex items-center justify-center transition-colors delay-100 duration-500',
			className
		)}
		{onclick}
		{onmouseenter}
		{onmouseleave}
	>
		{@render children()}
	</a>
{:else}
	<button
		type="button"
		use:action={{ active }}
		class={cn(
			'flex items-center justify-center transition-colors delay-100 duration-500',
			className
		)}
		{onclick}
		{onmouseenter}
		{onmouseleave}
	>
		{@render children()}
	</button>
{/if}
