<script lang="ts">
	import { formatPrice, getImageUrl } from '$lib/utils';
	import { fade, fly } from 'svelte/transition';
	import { Button } from './ui/button';
	import { enhance } from '$app/forms';
	import Input from './ui/input.svelte';
	import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';
	import * as Dialog from '$lib/components/ui/dialog';
	import ArrowRight from '@tabler/icons-svelte-runes/icons/arrow-right';

	let { artwork, index } = $props();

	let submitted = $state<Record<number, boolean>>({});
	let attemptedSubmit = $state<Record<number, boolean>>({});
	let loading = $state<Record<number, boolean>>({});

	// Reactive state maps per artwork index
	let formData = $state<
		Record<
			number,
			{ fullName: string; email: string; countryCode: string; phone: string; message: string }
		>
	>({});

	function getFormState(index: number) {
		return (
			formData[index] ?? { fullName: '', email: '', countryCode: '+250', phone: '', message: '' }
		);
	}

	function updateFormField(
		index: number,
		field: 'fullName' | 'email' | 'countryCode' | 'phone' | 'message',
		value: string
	) {
		if (!formData[index]) {
			formData[index] = { fullName: '', email: '', countryCode: '+250', phone: '', message: '' };
		}
		formData[index][field] = value;
	}

	function isValid(index: number) {
		const form = getFormState(index);
		return form.fullName.trim().length > 0 && /^\S+@\S+\.\S+$/.test(form.email);
	}

    const form = $derived(getFormState(index));
</script>

<div
	class={`space-y-6 pb-10 ${index < artwork.length - 1 ? 'border-b md:border-b-0 border-black/30' : ''} ${index < artwork.length - (artwork.length % 3 || 3) ? 'md:border-b md:border-black/30' : ''} rounded-3xl`}
>
	<img
		src={getImageUrl(artwork.image)}
		alt={artwork.name}
		loading="lazy"
		class="h-80 sm:h-100 md:h-120 w-full object-cover"
	/>

	<div class="space-y-8 text-[1rem]">
		<p class="font-display font-bold uppercase text-xl">{artwork.name}</p>

		<div class="grid grid-cols-2">
			<div class="border-r font-medium border-foreground/20 border-b py-3 pr-3">
				<p>Category</p>
				<p class="text-surface-foreground-muted font-normal">
					{artwork.category || 'N/A'}
				</p>
			</div>
			<div class="border-b font-medium border-foreground/20 p-3">
				<p>Year</p>
				<p class="text-surface-foreground-muted font-normal">
					{artwork.year || 'N/A'}
				</p>
			</div>

			<div class="border-r font-medium border-foreground/20 py-3 pr-3">
				<p>Medium</p>
				<p class="text-surface-foreground-muted font-normal">
					{artwork.medium || 'N/A'}
				</p>
			</div>

			<div class="font-medium p-3">
				<p>Dimensions</p>
				<p class="text-surface-foreground-muted font-normal">
					{artwork.dimensions || 'N/A'}
				</p>
			</div>
		</div>

		<div class={`${artwork.is_sold ? 'flex' : 'grid grid-cols-2'}  items-center place-items-start`}>
			<p class={`${artwork.is_sold ? 'hidden' : 'font-bold text-lg'}`}>
				{formatPrice({ price: artwork.price, currency: 'USD' })}
			</p>

			{#if artwork.is_sold}
				<Button
					color="secondary"
					variant="tonal"
					class="pointer-events-none rounded-none w-full uppercase text-md font-bold gap-4"
				>
					<p>Sold</p>
					<p>-</p>
					<p>{formatPrice({ price: artwork.price, currency: 'USD' })}</p>
				</Button>
			{:else}
				<Dialog.Root>
					<div class="px-3">
						<Dialog.Trigger>
							<Button color="black" variant="outline" class="rounded-none">
								<p>Inquire</p>
								<ArrowRight class="size-5" />
							</Button>
						</Dialog.Trigger>
					</div>

					<Dialog.Content
						class="z-60 fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-h-[85dvh] h-[90dvh] md:h-[75%] min-w-[95%] md:min-w-[90%] grid grid-cols-1 md:grid-cols-5 gap-4 p-0 overflow-y-auto md:overflow-hidden bg-transparent rounded-3xl"
					>
						<!-- Left Column: Artwork Specs & Preview -->
						<div
							class="md:col-span-3 bg-surface overflow-y-auto p-6 md:p-8 space-y-6 min-h-62.5 md:min-h-0"
						>
							<div class="relative w-full h-full min-h-62.5 overflow-hidden">
								<img
									src={getImageUrl(artwork.image)}
									alt={artwork.name}
									class="w-full h-full object-contain"
								/>
							</div>
						</div>

						<!-- Right Column: Inquiry Form -->
						<div class="bg-surface md:col-span-2 p-6 md:p-8 overflow-y-auto">
							{#if submitted[index]}
								<div
									in:fly={{ y: 20, duration: 400 }}
									out:fade={{ duration: 200 }}
									class="h-full flex flex-col items-center justify-center text-center gap-4 py-8 md:py-0"
								>
									<p class="font-display font-semibold text-2xl">Inquiry Sent</p>
									<p class="text-surface-foreground-muted max-w-xs text-sm">
										Thank you for your interest in <span class="font-semibold text-foreground"
											>"{artwork.name}"</span
										>. We will follow up with you by email shortly.
									</p>
								</div>
							{:else}
								<form
									method="POST"
									action="?/inquire"
									class="space-y-8"
									in:fade={{ duration: 300 }}
									out:fade={{ duration: 200 }}
									use:enhance={({ cancel }) => {
										attemptedSubmit[index] = true;
										if (!isValid(index)) {
											cancel();
											return;
										}

										loading[index] = true;

										return async ({ result }) => {
											loading[index] = false;

											if (result.type === 'success') {
												submitted[index] = true;
											}
										};
									}}
								>
									<input type="hidden" name="catalog_id" value={artwork.catalog_id} />
									<!-- Explicit hidden inputs so form action receives state values -->
									<input type="hidden" name="fullName" value={form.fullName} />
									<input type="hidden" name="email" value={form.email} />

									<div class="space-y-1">
										<p class="font-display font-semibold text-2xl">Artwork Inquiry</p>
										<p class="text-sm text-surface-foreground-muted">
											Complete the form below to inquire about acquiring this piece.
										</p>
									</div>

									<div class="space-y-6">
										<div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
											<div class="space-y-1">
												<Input
													label="Full Name *"
													context="surface"
													value={form.fullName}
													oninput={(e: Event) =>
														updateFormField(
															index,
															'fullName',
															(e.target as HTMLInputElement).value
														)}
												/>
												{#if attemptedSubmit[index] && !form.fullName.trim()}
													<p class="text-xs text-red-600">Name is required.</p>
												{/if}
											</div>

											<div class="space-y-1">
												<Input
													label="Email Address *"
													type="email"
													context="surface"
													value={form.email}
													oninput={(e: Event) =>
														updateFormField(index, 'email', (e.target as HTMLInputElement).value)}
												/>
												{#if attemptedSubmit[index] && !/^\S+@\S+\.\S+$/.test(form.email)}
													<p class="text-xs text-red-600">A valid email is required.</p>
												{/if}
											</div>
										</div>

										<div class="flex gap-1 items-end">
											<div class="flex flex-col w-20 space-y-2">
												<label for={`phone-code-${index}`} class="text-nowrap text-sm font-semibold"
													>Code</label
												>
												<Input
													context="surface"
													placeholder="+250"
													value={form.countryCode}
													oninput={(e: Event) =>
														updateFormField(
															index,
															'countryCode',
															(e.target as HTMLInputElement).value
														)}
													inputmode="tel"
													maxlength={6}
													class="rounded-r-none text-nowrap"
													id={`phone-code-${index}`}
												/>
											</div>
											<div class="flex-1 space-y-2">
												<label for={`phone-${index}`} class="text-nowrap text-sm font-semibold"
													>Phone number</label
												>
												<Input
													context="surface"
													placeholder="788 000 000"
													value={form.phone}
													oninput={(e: Event) =>
														updateFormField(index, 'phone', (e.target as HTMLInputElement).value)}
													inputmode="tel"
													class="rounded-l-none"
													id={`phone-${index}`}
												/>
											</div>
										</div>

										<input
											type="hidden"
											name="phone"
											value={`${form.countryCode} ${form.phone}`.trim()}
										/>

										<div class="space-y-2">
											<label for={`message-${index}`} class="text-sm font-semibold"
												>Message / Questions</label
											>
											<textarea
												id={`message-${index}`}
												name="message"
												rows="3"
												placeholder="Ask about shipping, framing, or custom arrangements..."
												value={form.message}
												oninput={(e: Event) =>
													updateFormField(
														index,
														'message',
														(e.target as HTMLTextAreaElement).value
													)}
												class="w-full bg-background border border-surface-border rounded-2xl p-4 text-sm focus:outline-hidden focus:border-black transition-colors resize-none"
											></textarea>
										</div>
									</div>

									<div class="pt-4 flex justify-end">
										<Button
											type="submit"
											disabled={loading[index] || (attemptedSubmit[index] && !isValid(index))}
											color="black"
											class="w-full"
										>
											{loading[index] ? 'Submitting...' : 'Send Inquiry'}
											<ArrowUpRight
												class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
											/>
										</Button>
									</div>
								</form>
							{/if}
						</div>
					</Dialog.Content>
				</Dialog.Root>
			{/if}
		</div>
	</div>
</div>
