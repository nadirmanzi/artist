<script lang="ts">
	import type { Component, Snippet } from 'svelte';

	interface Props {
		title: string;
		description?: string;
		icon?: Component<{ class?: string }>;
		action?: Snippet;
		class?: string;
	}

	let {
		title,
		description,
		icon: Icon,
		action,
		class: className = ''
	}: Props = $props();
</script>

<div
	class="flex flex-col items-center justify-center text-center p-8 sm:p-12 md:p-16 rounded-3xl bg-surface/70 border border-dashed border-black/15 transition-all duration-300 {className}"
>
	{#if Icon}
		<div
			class="mb-4 flex size-12 items-center justify-center rounded-2xl bg-background border border-black/10 text-foreground/70"
		>
			<Icon class="size-6 stroke-[1.5]" />
		</div>
	{/if}

	<h3 class="font-display text-xl sm:text-2xl font-semibold tracking-tight text-foreground">
		{title}
	</h3>

	{#if description}
		<p class="mt-2 max-w-md text-sm sm:text-base text-surface-foreground-muted leading-relaxed font-light">
			{description}
		</p>
	{/if}

	{#if action}
		<div class="mt-6 flex items-center justify-center gap-3">
			{@render action()}
		</div>
	{/if}
</div>
