<script lang="ts">
	import { enhance } from '$app/forms';
	import PageBanner from '$lib/components/page-banner.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import Input from '$lib/components/ui/input.svelte';
	import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';
	import type { StudioClass } from '$lib/api/types';
	import { animate } from '$lib/utils/animate';
	import { gsap } from 'gsap';
	import { formatPrice } from '$lib/utils';

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

	// Ticket "deal from the deck" tilt — same interaction language as the
	// homepage / catalog cards, tuned down slightly since these cards are
	// less square.
	function tiltCard(e: MouseEvent) {
		const card = e.currentTarget as HTMLElement;
		const rect = card.getBoundingClientRect();
		const px = (e.clientX - rect.left) / rect.width;
		const py = (e.clientY - rect.top) / rect.height;

		gsap.to(card, {
			rotateX: (py - 0.5) * -30,
			rotateY: (px - 0.5) * 30,
			y: -4,
			duration: 0.5,
			ease: 'power2.out',
			transformPerspective: 900,
			transformOrigin: 'center'
		} as gsap.TweenVars);
	}

	function resetCard(e: MouseEvent) {
		gsap.to(
			e.currentTarget as HTMLElement,
			{
				rotateX: 0,
				rotateY: 0,
				y: 0,
				duration: 0.6,
				ease: 'power3.out'
			} as gsap.TweenVars
		);
	}
</script>

<PageBanner text="Learn to paint. Learn to see." image="/images/book-class.png" />

<div class="bg-surface px-6 sm:px-12 lg:px-20 pt-16 md:pt-24 pb-6">
	<div
		class="max-w-2xl"
		use:animate={{
			type: 'from',
			opacity: 0,
			y: 30,
			ease: 'none',
			scrollTrigger: { start: 'top 95%', end: 'top 75%', scrub: true }
		}}
	>
		<p class="font-mono text-xs tracking-[0.25em] uppercase text-surface-foreground-muted">
			Studio Sessions
		</p>
		<p class="font-display font-semibold text-3xl sm:text-4xl mt-2">
			Pick a class, reserve your seat.
		</p>
	</div>
</div>

<div class="bg-surface px-6 sm:px-12 lg:px-20 pb-16 md:pb-28">
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
		{#each classes as lesson, index (lesson.studio_class_id ?? lesson.name)}
			{@const form = getFormState(index)}
			<div
				class="relative bg-background flex flex-col justify-between rounded-[28px] overflow-hidden duration-300 transform-3d will-change-transform"
				onmousemove={tiltCard}
				onmouseleave={resetCard}
				role="contentinfo"
			>
				<div class="p-6 sm:p-8 space-y-5">
					<p
						class="font-display font-semibold text-2xl underline underline-offset-8 decoration-solid"
					>
						{lesson.name}
					</p>

					<p class="text-surface-foreground-muted text-[0.95rem]">{lesson.description}</p>
				</div>

				<div class="p-6 sm:p-8 pt-6">
					<Dialog.Root>
						<Dialog.Trigger class="w-full">
							<Button color="black" variant="outline" class="w-full">
								<p>Book this class</p>
								<ArrowUpRight
									class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-1"
								/>
							</Button>
						</Dialog.Trigger>

						<Dialog.Content
							class="z-60 fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-h-[85dvh] h-[90dvh] lg:h-[75%] min-w-[95%] sm:min-w-[90%] lg:min-w-[85%] grid grid-cols-1 lg:grid-cols-5 gap-4 p-0 overflow-y-auto lg:overflow-hidden bg-transparent rounded-3xl  isolate"
						>
							<!-- Left Column: Class Details & Programs -->
							<div
								class="lg:col-span-3 bg-surface overflow-y-auto space-y-12 border-b lg:border-b-0 p-8 lg:border-r border-dashed border-black/20"
							>
								<div class="relative overflow-hidden space-y-6 sm:space-y-8">
									<p
										class="font-display font-semibold text-3xl sm:text-4xl pr-16 sm:pr-20 text-foreground"
									>
										{lesson.name}
									</p>
									<p class="w-full text-sm text-surface-foreground-muted font-medium">
										{lesson.description}
									</p>
								</div>

								<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
									{#each lesson.programs as program (program.program_id ?? program.name)}
										<div class="group/card space-y-2 sm:space-y-4 rounded-3xl p-5 flex flex-col justify-between bg-background">
											<p class="font-bold text-[1.1rem] text-foreground">{program.name}</p>

											<div class="space-y-2 text-sm sm:text-base">
													<p class="font-semibold">Includes:</p>
													<ul
														class="space-y-1 sm:space-y-2 font-medium text-surface-foreground-muted text-sm"
													>
														{#each program.includes as item, itemIdx (itemIdx)}
															<li>- {item}</li>
														{/each}
													</ul>
											</div>
											<div
												class="mt-6 sm:mt-8 tracking-wide flex items-center space-x-4 font-semibold"
											>
												<p class="">
													{formatPrice(program.price)}
												</p>
												<p>/</p>
												<p>{program.sessions} <span class="text-surface-foreground-muted">{program.sessions > 1 ? 'sessions' : 'session'}</span></p>
											</div>
										</div>
									{/each}
								</div>
							</div>

							<!-- Right Column: Booking Form -->
							<div class="bg-surface lg:col-span-2 p-4 sm:p-6 overflow-y-auto">
								{#if submitted[index]}
									<div
										class="h-full min-h-[300px] flex flex-col items-center justify-center text-center gap-4 py-8"
									>
										<div
											class="w-24 h-24 rounded-full border-2 border-dashed flex items-center justify-center -rotate-6"
											style="border-color: #9a3324; color: #9a3324;"
											aria-hidden="true"
										>
											<span class="font-mono text-[10px] tracking-[0.15em] uppercase font-bold"
												>Confirmed</span
											>
										</div>
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
															updateFormField(
																index,
																'fullName',
																(e.target as HTMLInputElement).value
															)}
													/>
													{#if attemptedSubmit[index] && !form.fullName.trim()}
														<p class="text-xs text-destructive">Name is required.</p>
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
														<p class="text-xs text-destructive">A valid email is required.</p>
													{/if}
												</div>
											</div>

											<div class="flex gap-1 items-end">
												<div class="flex flex-col w-20 space-y-2">
													<label
														for={`phone-code-${index}`}
														class="text-nowrap text-sm font-semibold">Code</label
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
															class="flex items-center gap-4 bg-background cursor-pointer rounded-2xl border border-dashed border-black/15 px-5 py-4 transition-colors hover:border-black/40 peer-checked:border-solid peer-checked:border-foreground peer-checked:bg-foreground peer-checked:text-white peer-focus-visible:ring-2 peer-focus-visible:ring-black peer-focus-visible:ring-offset-2"
														>
															<span
																class="shrink-0 font-mono text-[10px] w-6 h-6 rounded-full border border-current flex items-center justify-center opacity-60"
															>
																{String.fromCharCode(65 + pIndex)}
															</span>
															<span class="flex-1 font-medium text-sm sm:text-base"
																>{program.name}</span
															>
															<span class="font-mono text-xs sm:text-sm opacity-70"
																>{formatPrice(program.price)}</span
															>
														</label>
													</div>
												{/each}

												{#if attemptedSubmit[index] && !selectedProgram[index]}
													<p class="text-xs text-destructive">Please select a program.</p>
												{/if}
											</div>
										</div>

										<div class="pt-4 border-t border-dashed border-black/20 flex justify-end">
											<Button
												type="submit"
												disabled={loading[index] || (attemptedSubmit[index] && !isValid(index))}
												color="black"
												class="w-full font-mono uppercase tracking-[0.15em] text-xs"
											>
												{loading[index] ? 'Booking...' : 'Confirm booking'}
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
			</div>
		{/each}
	</div>
</div>
