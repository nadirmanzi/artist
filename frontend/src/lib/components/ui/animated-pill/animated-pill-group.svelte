<script module lang="ts">
	import { getContext } from 'svelte';
	import type { Action } from 'svelte/action';

	export interface PillGroupContext {
		register: (id: string, el: HTMLElement) => () => void;
		setActive: (id: string | null) => void;
		activeId: () => string | null;
		/**
		 * A highly optimized Svelte Action that automatically binds any HTML element
		 * to the Pill Group physics engine. It tracks hover states, 'data-highlighted'
		 * attributes (for Bits UI), and declarative 'active' states effortlessly.
		 */
		pillTracker: Action<HTMLElement, { active?: boolean; id?: string } | undefined>;
	}

	export function getPillGroup(): PillGroupContext | undefined {
		return getContext<PillGroupContext>('pill-group');
	}
</script>

<script lang="ts">
	/*
	 * ─── ANIMATED PILL GROUP ───────────────────────────────────────────────────
	 * A sophisticated layout container that manages a single "sliding pill"
	 * background shared across multiple child items.
	 * ───────────────────────────────────────────────────────────────────────────────
	 */
	import { setContext } from 'svelte';
	import { SvelteMap } from 'svelte/reactivity';
	import { cn } from '$lib/utils';

	let {
		color = 'var(--color-surface-hover)',
		rounded = 'rounded-full',
		direction = 'horizontal',
		class: className,
		children
	}: {
		/**
		 * Can be any valid CSS color or variable (e.g. 'var(--color-primary)')
		 */
		color?: string;
		rounded?: string;
		direction?: 'horizontal' | 'vertical';
		class?: string;
		children: import('svelte').Snippet;
	} = $props();

	// ─── STATE ───────────────────────────────────────────────────────────────────
	let mounted = $state(false);
	let activeId = $state<string | null>(null);
	let defaultActiveId = $state<string | null>(null);
	let container = $state<HTMLElement | null>(null);

	let pillWidth = $state(0);
	let pillHeight = $state(0);
	let pillTransform = $state('translate3d(0,0,0)');
	let isVisible = $state(false);

	const items = new SvelteMap<string, HTMLElement>();
	let isGroupHovered = $state(false);

	function setActive(id: string | null) {
		if (id) {
			activeId = id;
		} else if (!isGroupHovered) {
			activeId = defaultActiveId;
		}
	}

	// ─── ACTION ──────────────────────────────────────────────────────────────────
	const pillTracker: Action<HTMLElement, { active?: boolean; id?: string } | undefined> = (
		node,
		params = {}
	) => {
		const id = params.id || Math.random().toString(36).slice(2);

		items.set(id, node);
		const unregister = () => items.delete(id);

		const handleEnter = () => setActive(id);
		const handleLeave = () => {
			if (activeId === id) setActive(null);
		};

		node.addEventListener('mouseenter', handleEnter);
		node.addEventListener('mouseleave', handleLeave);

		// Observe 'data-highlighted' for native Bits UI dropdown/select support
		const observer = new MutationObserver((mutations) => {
			for (const m of mutations) {
				if (m.attributeName === 'data-highlighted') {
					if (node.hasAttribute('data-highlighted')) setActive(id);
					else if (activeId === id) setActive(null);
				}
			}
		});
		observer.observe(node, { attributes: true, attributeFilter: ['data-highlighted'] });

		if (params?.active) {
			defaultActiveId = id;
			setActive(id);
		}

		return {
			update(newParams) {
				if (newParams?.active && !params?.active) {
					defaultActiveId = id;
					if (!isGroupHovered) setActive(id);
				} else if (params?.active && !newParams?.active) {
					if (defaultActiveId === id) defaultActiveId = null;
					if (activeId === id && !isGroupHovered) setActive(null);
				} else if (newParams?.active) {
					defaultActiveId = id; // Ensure default is maintained if it updates while active
				}
				params = newParams || {};
			},
			destroy() {
				node.removeEventListener('mouseenter', handleEnter);
				node.removeEventListener('mouseleave', handleLeave);
				observer.disconnect();
				unregister();
			}
		};
	};

	// ─── CONTEXT ─────────────────────────────────────────────────────────────────
	setContext<PillGroupContext>('pill-group', {
		register: (id, el) => {
			items.set(id, el);
			return () => items.delete(id);
		},
		setActive,
		activeId: () => activeId,
		pillTracker
	});

	// ─── MEASUREMENT & PHYSICS ──────────────────────────────────────────────────
	function updatePill() {
		if (!container) return;
		if (!activeId) {
			isVisible = false;
			return;
		}

		const activeEl = items.get(activeId);
		if (activeEl) {
			const rect = activeEl.getBoundingClientRect();
			const containerRect = container.getBoundingClientRect();

			pillWidth = rect.width;
			pillHeight = rect.height;
			pillTransform = `translate3d(${rect.left - containerRect.left}px, ${rect.top - containerRect.top}px, 0)`;
			isVisible = true;
		}
	}

	$effect(() => {
		mounted = true;
		if (!container) return;
		const observer = new ResizeObserver(updatePill);
		observer.observe(container);
		return () => observer.disconnect();
	});

	$effect(updatePill);
</script>

<div
	bind:this={container}
	class={cn(
		'relative flex h-full items-center',
		direction === 'vertical' ? 'w-full flex-col' : 'justify-center'
	)}
	onmouseenter={() => (isGroupHovered = true)}
	onmouseleave={() => {
		isGroupHovered = false;
		activeId = defaultActiveId;
	}}
	role="presentation"
>
	{#if mounted}
		<div
			class={cn(
				'pointer-events-none absolute top-0 left-0 z-0 transition-[transform,width,height,opacity] delay-100 duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)]',
				rounded
			)}
			style="
				width: {pillWidth}px;
				height: {pillHeight}px;
				transform: {pillTransform};
				opacity: {isVisible ? 1 : 0};
				background: {color};
			"
		></div>
	{/if}

	<div
		class={cn(
			'relative z-10 flex h-full w-full',
			direction === 'vertical' ? 'flex-col' : '',
			className
		)}
	>
		{@render children()}
	</div>
</div>
