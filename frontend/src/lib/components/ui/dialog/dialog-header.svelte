<script lang="ts">
	import type { HTMLAttributes } from "svelte/elements";
	import { Dialog as DialogPrimitive } from "bits-ui";
	import { cn, type WithElementRef } from "$lib/utils.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import { IconX } from '@tabler/icons-svelte-runes';

	let {
		ref = $bindable(null),
		class: className,
		children,
		...restProps
	}: WithElementRef<HTMLAttributes<HTMLDivElement>> = $props();
</script>

<div
	bind:this={ref}
	data-slot="dialog-header"
	class={cn("gap-2 flex flex-col", className)}
	{...restProps}
>
	{@render children?.()}
			<DialogPrimitive.Close data-slot="dialog-close">
				{#snippet child({ props })}
					<Button variant="ghost" color='black'  class="absolute top-4 right-4" size='icon' {...props}>
						<IconX  strokeWidth={2} class='size-5' />
						<span class="sr-only">Close</span>
					</Button>
				{/snippet}
			</DialogPrimitive.Close>
</div>
