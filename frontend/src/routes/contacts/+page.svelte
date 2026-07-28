<script lang="ts">
	import { enhance } from '$app/forms';
	import { fade, fly } from 'svelte/transition';
	import PageBanner from '$lib/components/page-banner.svelte';
	import Mail from '@tabler/icons-svelte-runes/icons/mail';
	import Phone from '@tabler/icons-svelte-runes/icons/phone';
	import MapPin from '@tabler/icons-svelte-runes/icons/map-pin';
	import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';
	import Button from '$lib/components/ui/button/button.svelte';

	// Form states using Svelte 5 runes
	let name = $state('');
	let email = $state('');
	let phone = $state('');
	let message = $state('');

	let loading = $state(false);
	let submitted = $state(false);
	let errorMessage = $state('');

	let instagram_link: string = $state(
		'https://www.instagram.com/studio_mugire__?igsh=MWk1cHB2Z29mYnNuOA=='
	);
</script>

<PageBanner text="Let’s Begin a Conversation" image="/images/contact-banner.png" />

<div
	class="px-6 sm:px-12 md:px-20 py-16 md:py-24 max-w-7xl mx-auto flex flex-col lg:flex-row items-start justify-between gap-12 lg:gap-20"
>
	<!-- Left Column: Artistic Copy & Quick Direct Info -->
	<div class="w-full lg:w-1/2 lg:sticky lg:top-12">
		<div class="space-y-6 pb-12">
			<span
				class="inline-block text-xs uppercase tracking-widest font-semibold text-secondary"
			>
				Connect with the Studio
			</span>
			<p
				class="text-surface-foreground-muted text-base md:text-lg font-light max-w-md leading-relaxed pt-2"
			>
				Whether you are looking to collect an artwork, commission a piece, visit the studio, join a
				creative experience, or explore a collaboration, we would love to hear from you.
			</p>
		</div>

		<!-- Direct Contact Quick List -->
		<div class="border-t border-surface-border/60 pt-10 space-y-8">
			<div class="flex items-center gap-4 group cursor-pointer">
				<div class="rounded-full bg-transparent text-on-secondary transition-all duration-300">
					<Mail stroke-width={2} class="w-5 h-5 text-secondary" />
				</div>
				<a href="mailto:studio@mugire.com" class="text-sm md:text-base text-foreground">
					mpeacedavid@gmail.com
				</a>
			</div>

			<div class="flex items-center gap-4 group cursor-pointer">
				<div class="rounded-full bg-transparent text-on-secondary transition-all duration-300">
					<Phone stroke-width={2} class="w-5 h-5 text-secondary" />
				</div>
				<a href="tel:+1234567890" class="text-sm md:text-base text-foreground">
					+250 784 446 662
				</a>
			</div>

			<div class="flex items-center gap-4 group">
				<div class="rounded-full bg-transparent text-on-secondary transition-all duration-300">
					<MapPin stroke-width={2} class="w-5 h-5 text-secondary" />
				</div>
				<p class="text-sm md:text-base text-foreground leading-snug">
					KN54 st Kiyovu, Kigali, Rwanda
				</p>
			</div>
		</div>
	</div>

	<!-- Right Column: Elevated Atelier Form -->
	<div class="w-full lg:w-1/2 xl:w-5/12">
		<div
			class="bg-transparent rounded-3xl p-8 sm:p-10 transition-all duration-500 hover:border-surface-border"
		>
			{#if submitted}
				<div
					in:fly={{ y: 20, duration: 400 }}
					out:fade={{ duration: 200 }}
					class="py-12 text-center space-y-6"
				>
					<div
						class="w-12 h-12 rounded-full bg-foreground/5 text-foreground mx-auto flex items-center justify-center"
					>
						<ArrowUpRight class="w-6 h-6" />
					</div>
					<div class="space-y-2">
						<h3 class="font-display font-light text-3xl text-foreground">Inquiry Received</h3>
						<p class="text-surface-foreground-muted text-sm leading-relaxed max-w-xs mx-auto">
							Thank you for reaching out. We have received your message and will respond within 24
							hours.
						</p>
					</div>
					<button
						type="button"
						onclick={() => {
							submitted = false;
							name = '';
							email = '';
							phone = '';
							message = '';
						}}
						class="inline-block text-xs uppercase tracking-widest font-medium border-b border-foreground/30 hover:border-foreground text-foreground/80 hover:text-foreground transition-all pt-2"
					>
						Send another message
					</button>
				</div>
			{:else}
				<form
					method="POST"
					class="space-y-8"
					in:fade={{ duration: 300 }}
					use:enhance={() => {
						loading = true;
						errorMessage = '';

						return async ({ result }) => {
							loading = false;

							if (result.type === 'success') {
								submitted = true;
							} else if (result.type === 'failure') {
								errorMessage =
									(result.data?.error as string) || 'An error occurred while sending your inquiry.';
							}
						};
					}}
				>
					{#if errorMessage}
						<div
							in:fly={{ y: -10, duration: 200 }}
							class="p-4 bg-red-500/10 text-red-600 text-xs rounded-xl border border-red-500/20 font-medium"
						>
							{errorMessage}
						</div>
					{/if}

					<!-- Grid Fields -->
					<div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
						<!-- Full Name -->
						<div class="relative group">
							<input
								id="name"
								name="name"
								type="text"
								bind:value={name}
								required
								placeholder=" "
								class="peer w-full bg-transparent border-b border-surface-border py-2.5 text-foreground text-sm focus:outline-none transition-colors"
							/>
							<label
								for="name"
								class="absolute left-0 top-2.5 text-sm text-surface-foreground-muted transition-all duration-200 pointer-events-none peer-focus:-top-4 peer-focus:text-xs peer-focus:text-foreground peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:text-foreground"
							>
								Full Name *
							</label>
							<span
								class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"
							></span>
						</div>

						<!-- Email -->
						<div class="relative group">
							<input
								id="email"
								name="email"
								type="email"
								bind:value={email}
								required
								placeholder=" "
								class="peer w-full bg-transparent border-b border-surface-border py-2.5 text-foreground text-sm focus:outline-none transition-colors"
							/>
							<label
								for="email"
								class="absolute left-0 top-2.5 text-sm text-surface-foreground-muted transition-all duration-200 pointer-events-none peer-focus:-top-4 peer-focus:text-xs peer-focus:text-foreground peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:text-foreground"
							>
								Email Address *
							</label>
							<span
								class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"
							></span>
						</div>
					</div>

					<!-- Phone Contact -->
					<div class="relative group">
						<input
							id="phone"
							name="phone"
							type="tel"
							bind:value={phone}
							placeholder=" "
							class="peer w-full bg-transparent border-b border-surface-border py-2.5 text-foreground text-sm focus:outline-none transition-colors"
						/>
						<label
							for="phone"
							class="absolute left-0 top-2.5 text-sm text-surface-foreground-muted transition-all duration-200 pointer-events-none peer-focus:-top-4 peer-focus:text-xs peer-focus:text-foreground peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:text-foreground"
						>
							Phone Number (Optional)
						</label>
						<span
							class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"
						></span>
					</div>

					<!-- Message / Inquiry Box -->
					<div class="relative group pt-2">
						<textarea
							id="message"
							name="message"
							bind:value={message}
							required
							rows="3"
							placeholder=" "
							class="peer w-full bg-transparent border-b border-surface-border py-2.5 text-foreground text-sm resize-none focus:outline-none transition-colors"
						></textarea>
						<label
							for="message"
							class="absolute left-0 top-4 text-sm text-surface-foreground-muted transition-all duration-200 pointer-events-none peer-focus:-top-2 peer-focus:text-xs peer-focus:text-foreground peer-[:not(:placeholder-shown)]:-top-2 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:text-foreground"
						>
							Describe your project or inquiry *
						</label>
						<span
							class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"
						></span>
					</div>

					<!-- Submit Button -->
					<div class="flex justify-end">
						<Button disabled={loading} type="submit" class="w-full" color='black'>
							<span>{loading ? 'Sending...' : 'Send Inquiry'}</span>
							<ArrowUpRight
								class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
							/>
						</Button>
					</div>
				</form>
			{/if}
		</div>

		<!-- Social Channels Section -->
		<div class="pt-10 space-y-3 text-start lg:text-end">
			<h4 class="text-[10px] uppercase tracking-widest text-surface-foreground-muted font-semibold">
				Follow the Process
			</h4>
			<div class="flex flex-wrap justify-start lg:justify-end gap-x-6 gap-y-2 text-sm">
				<a
					href={instagram_link}
					target="_blank"
					rel="noopener noreferrer"
					class="text-foreground underline transition-colors flex items-center gap-1 group py-1"
				>
					<span>Instagram</span>
					<ArrowUpRight
						class="w-3.5 h-3.5 opacity-40 group-hover:opacity-100 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all"
					/>
				</a>
			</div>
		</div>
	</div>
</div>
