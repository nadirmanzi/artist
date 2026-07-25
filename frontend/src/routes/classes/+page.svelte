<script lang="ts">
	import { enhance } from '$app/forms';
	import PageBanner from '$lib/components/page-banner.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import Input from '$lib/components/ui/input.svelte';
	import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';
	import type { StudioClass } from '$lib/api/types';

	let { data }: { data: { classes: StudioClass[] } } = $props();

	const classes = $derived(data.classes ?? []);

	// Reactive state maps per class card index
	let selectedProgram = $state<Record<number, string>>({});
	let formData = $state<
		Record<number, { fullName: string; email: string; countryCode: string; phone: string }>
	>({});
	let submitted = $state<Record<number, boolean>>({});
	let attemptedSubmit = $state<Record<number, boolean>>({});
	let loading = $state<Record<number, boolean>>({});

	// Read-only getter — safe to invoke during rendering
	function getFormState(index: number) {
		return formData[index] ?? { fullName: '', email: '', countryCode: '+250', phone: '' };
	}

	// Explicit state updater for input events
	function updateFormField(
		index: number,
		field: 'fullName' | 'email' | 'countryCode' | 'phone',
		value: string
	) {
		if (!formData[index]) {
			formData[index] = { fullName: '', email: '', countryCode: '+250', phone: '' };
		}
		formData[index][field] = value;
	}

	function isValid(index: number) {
		const form = getFormState(index);
		const program = selectedProgram[index] ?? '';
		return form.fullName.trim().length > 0 && /^\S+@\S+\.\S+$/.test(form.email) && program !== '';
	}
</script>

<PageBanner text="Learn to paint. Learn to see." image="/images/book-class.png" />

<div
	class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 p-6 sm:p-12 lg:p-20 gap-8 md:gap-0 bg-surface"
>
	{#each classes as lesson, index (lesson.studio_class_id ?? lesson.name)}
		{@const form = getFormState(index)}
		{@const total = classes.length}
		<div
			class={`p-6 sm:p-8 border-black/20 space-y-8 flex flex-col justify-between
                ${index > 0 ? 'border-t md:border-t-0' : ''}
                ${total === 2 && index === 1 ? 'md:border-l lg:border-l' : ''}
                ${total >= 3 && index % 3 !== 0 ? 'md:border-l lg:border-l' : ''}
                ${total >= 3 && index % 3 === 0 && index > 0 ? 'md:border-l-0' : ''}
            `}
		>
			<div class="space-y-6">
				<div class="space-y-2">
					<p
						class="font-display font-semibold text-2xl underline underline-offset-8 decoration-solid"
					>
						{lesson.name}
					</p>
				</div>

				<div>
					<p class="text-surface-foreground-muted">{lesson.description}</p>
				</div>
			</div>

			<Dialog.Root>
				<Dialog.Trigger class="mt-8 w-full">
					<Button class="w-full" color="black" variant="tonal">Book Now</Button>
				</Dialog.Trigger>

				<Dialog.Content
					class="z-[60] fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-h-[85dvh] h-[90dvh] lg:h-[75%] min-w-[95%] sm:min-w-[90%] lg:min-w-[85%] grid grid-cols-1 lg:grid-cols-5 gap-0 p-0 overflow-y-auto lg:overflow-hidden bg-transparent rounded-3xl"
				>
					<!-- Left Column: Class Details & Programs -->
					<div
						class="lg:col-span-3 bg-surface overflow-y-auto space-y-2 border-b lg:border-b-0 lg:border-r border-black/10"
					>
						<div class="p-4 sm:p-6">
							<div class="space-y-6 sm:space-y-8 p-6 sm:p-10 bg-foreground text-white rounded-3xl">
								<p class="font-display font-semibold text-3xl sm:text-4xl">
									{lesson.name}
								</p>
								<p class="w-full text-sm sm:text-base">{lesson.description}</p>
							</div>
						</div>

						<div class="space-y-6 sm:space-y-8 p-4 sm:p-6">
							<p class="text-lg sm:text-xl font-bold">Programs offered</p>

							<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
								{#each lesson.programs as program (program.program_id ?? program.name)}
									<div class="space-y-4 sm:space-y-6 bg-background p-5 sm:p-8 rounded-3xl">
										<p class="font-semibold text-[1rem]">{program.name}</p>

										<div class="space-y-2 text-sm sm:text-base">
											<p class="font-semibold">
												Sessions:
												<span class="text-surface-foreground-muted font-normal">
													{program.sessions} session{program.sessions === 1 ? '' : 's'}
												</span>
											</p>

											<div class="space-y-2">
												<p class="font-semibold">Includes:</p>
												<ul class="space-y-1 sm:space-y-2 text-surface-foreground-muted">
													{#each program.includes as item, itemIdx (itemIdx)}
														<li>- {item}</li>
													{/each}
												</ul>
											</div>

											<p class="font-semibold mt-4 sm:mt-6">
												Price: <span class="font-semibold underline">{program.price}</span>
											</p>
										</div>
									</div>
								{/each}
							</div>
						</div>
					</div>

					<!-- Right Column: Booking Form -->
					<div class="bg-surface lg:col-span-2 p-4 sm:p-6 overflow-y-auto">
						{#if submitted[index]}
							<div
								class="h-full min-h-[300px] flex flex-col items-center justify-center text-center gap-4 py-8"
							>
								<p class="font-display font-semibold text-2xl">Booking confirmed</p>
								<p class="text-surface-foreground-muted max-w-xs text-sm">
									Thanks for booking {lesson.name.toLowerCase()} — we'll follow up by email shortly.
								</p>
							</div>
						{:else}
							<form
								method="POST"
								action="?/book"
								class="space-y-8 sm:space-y-10"
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
								<!-- Form payload values -->
								<input type="hidden" name="catalog_id" value={selectedProgram[index] ?? ''} />
								<input type="hidden" name="fullName" value={form.fullName} />
								<input type="hidden" name="email" value={form.email} />
								<input
									type="hidden"
									name="phone"
									value={`${form.countryCode} ${form.phone}`.trim()}
								/>

								<div class="space-y-1">
									<p class="font-display font-semibold text-2xl">Your details</p>
									<p class="text-sm text-surface-foreground-muted">
										We'll use this to confirm your spot.
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
													updateFormField(index, 'fullName', (e.target as HTMLInputElement).value)}
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
								</div>

								<div class="space-y-4">
									<p class="font-semibold">Select a program *</p>

									<div class="space-y-3">
										{#if lesson.programs.length === 0}
											<p class="text-sm text-surface-foreground-muted">
												No active programs are available for this class.
											</p>
										{/if}
										{#each lesson.programs as program, pIndex (program.program_id ?? program.name)}
											{@const inputId = `program-${index}-${pIndex}`}
											<div class="rounded-2xl">
												<input
													type="radio"
													id={inputId}
													name={`program-group-${index}`}
													value={program.program_id ?? program.name}
													bind:group={selectedProgram[index]}
													class="peer sr-only"
												/>
												<label
													for={inputId}
													class="flex items-center justify-between bg-background gap-4 cursor-pointer rounded-2xl border border-black/10 px-5 py-4 transition-colors hover:border-black/30 peer-checked:border-black peer-checked:bg-black peer-checked:text-white peer-focus-visible:ring-2 peer-focus-visible:ring-black peer-focus-visible:ring-offset-2"
												>
													<span class="font-medium text-sm sm:text-base">{program.name}</span>
													<span class="text-xs sm:text-sm opacity-70">{program.price}</span>
												</label>
											</div>
										{/each}

										{#if attemptedSubmit[index] && !selectedProgram[index]}
											<p class="text-xs text-red-600">Please select a program.</p>
										{/if}
									</div>
								</div>

								<div class="pt-4 flex justify-end">
									<Button
										type="submit"
										disabled={loading[index] || (attemptedSubmit[index] && !isValid(index))}
										color="black"
										class="w-full"
									>
										{loading[index] ? 'Booking...' : 'Book this class'}
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
		</div>
	{/each}
</div>
