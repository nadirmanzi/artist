<script lang="ts">
	import PageBanner from '$lib/components/page-banner.svelte';
	import Mail from '@tabler/icons-svelte-runes/icons/mail';
	import Phone from '@tabler/icons-svelte-runes/icons/phone';
	import MapPin from '@tabler/icons-svelte-runes/icons/map-pin';
	import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';

	// Form states
	let name = $state('');
	let email = $state('');
	let phone = $state('');
	let message = $state('');

	function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		// Handle form action here
	}
</script>

<PageBanner text="Bring Your Vision To The Canvas." image="/contact4.jpg" />

<div class=" py-20 flex items-start justify-center gap-50">
	<!-- Left Column: Artistic Copy & Quick Direct Info -->
	<div class="">
		<div class="space-y-4 pb-10">
			<span class="text-sm font-medium text-surface-foreground-muted">Connect with the Studio</span>
			<h1 class="text-5xl font-display font-light text-foreground leading-tight">
				Let’s co-create <br /> something

				<span class="relative inline-block italic text-foreground/50">
					permanent
					<svg
						class="ink-underline absolute -bottom-3 left-0 w-full"
						viewBox="0 0 160 12"
						preserveAspectRatio="none"
						aria-hidden="true"
					>
						<path
							d="M2 8.5 C 30 3, 60 10, 88 5 S 140 2, 158 6"
							fill="none"
							stroke="var(--color-surface-foreground-muted)"
							stroke-width="2"
							stroke-linecap="round"
							pathLength="1"
						/>
					</svg>
				</span>
			</h1>
			<p class="text-surface-foreground-muted text-base font-light max-w-md leading-relaxed pt-2">
				Whether you're looking to acquire an original piece, enroll in an masterclass, or commission
				custom work—our doors are open.
			</p>
		</div>

		<!-- Direct Contact Quick Grid -->
		<div class="border-t border-black/20 py-10 space-y-6">
			<div class="flex items-start gap-4 group">
				<div
					class="p-2 rounded-full bg-black/5 text-black/70 group-hover:bg-black group-hover:text-white transition-colors duration-300"
				>
					<Mail class="w-4 h-4" />
				</div>
				<div>
					<h4 class="text-xs uppercase tracking-wider text-black/40 font-medium">Inquiries</h4>
					<a
						href="mailto:studio@mugire.com"
						class="text-sm text-black/80 hover:text-black transition-colors">studio@mugire.com</a
					>
				</div>
			</div>

			<div class="flex items-start gap-4 group">
				<div
					class="p-2 rounded-full bg-black/5 text-black/70 group-hover:bg-black group-hover:text-white transition-colors duration-300"
				>
					<Phone class="w-4 h-4" />
				</div>
				<div>
					<h4 class="text-xs uppercase tracking-wider text-black/40 font-medium">
						Call the Atelier
					</h4>
					<a href="tel:+1234567890" class="text-sm text-black/80 hover:text-black transition-colors"
						>+1 (234) 567-890</a
					>
				</div>
			</div>

			<div class="flex items-start gap-4 group">
				<div
					class="p-2 rounded-full bg-black/5 text-black/70 group-hover:bg-black group-hover:text-white transition-colors duration-300"
				>
					<MapPin class="w-4 h-4" />
				</div>
				<div>
					<h4 class="text-xs uppercase tracking-wider text-black/40 font-medium">Visit Us</h4>
					<p class="text-sm text-black/80">104 Beaux-Arts Blvd, Suite 400<br />Paris, NY 10013</p>
				</div>
			</div>
		</div>
	</div>

	<div class="w-1/3">
		<!-- Right Column: Premium Floating Form Interface -->
		<div class="bg-surface border border-surface-border rounded-3xl p-8">
			<form onsubmit={handleSubmit} class="space-y-8">
				<!-- Grid Fields -->
				<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
					<!-- Full Name -->
					<div class="relative group">
						<label class="text-sm"> Full Name * </label>
						<input
							type="text"
							bind:value={name}
							required
							placeholder=" "
							class="w-full bg-transparent border-b border-black/20 py-2 text-black text-sm focus:outline-hidden focus:border-black transition-colors peer"
						/>
					</div>

					<!-- Email -->
					<div class="relative group">
						<label class="text-sm"> Email Address * </label>
						<input
							type="email"
							bind:value={email}
							required
							placeholder=" "
							class="w-full bg-transparent border-b border-black/20 py-2 text-black text-sm focus:outline-hidden focus:border-black transition-colors peer"
						/>
					</div>
				</div>

				<!-- Number Contact -->
				<div class="relative group">
					<label class="text-sm"> Phone Number (Optional) </label>
					<input
						type="tel"
						bind:value={phone}
						placeholder=" "
						class="w-full bg-transparent border-b border-black/20 py-2 text-black text-sm focus:outline-hidden focus:border-black transition-colors peer"
					/>
				</div>

				<!-- Message / Inquiry Box -->
				<div class="relative group pt-4">
					<label class="text-sm"> Describe your project or inquiry * </label>
					<textarea
						bind:value={message}
						required
						rows="2"
						placeholder=" "
						class="w-full bg-transparent border-b border-black/20 py-3 text-black text-sm resize-none focus:outline-hidden focus:border-black transition-colors peer"
					></textarea>
				</div>

				<!-- Premium Submit Button -->
				<div class="pt-4 flex justify-end">
					<button
						type="submit"
						class="bg-black hover:bg-black/90 text-white text-sm tracking-wider uppercase py-4 px-8 rounded-full flex items-center gap-2 group transition-all duration-300 shadow-lg shadow-black/5"
					>
						Send Inquiry
						<ArrowUpRight
							class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
						/>
					</button>
				</div>
			</form>
		</div>

		<!-- Social Channels Section -->
		<div class="py-10 space-y-3 text-end">
			<h4 class="text-xs uppercase tracking-wider text-black/40 font-medium">Follow the Process</h4>
			<div class="flex flex-wrap justify-end gap-x-6 gap-y-2 text-sm">
				<a
					href="https://instagram.com"
					target="_blank"
					rel="noopener noreferrer"
					class="text-black/60 hover:text-black transition-colors flex items-center gap-0.5 group"
				>
					<ArrowUpRight class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
					Instagram
				</a>
				<a
					href="https://pinterest.com"
					target="_blank"
					rel="noopener noreferrer"
					class="text-black/60 hover:text-black transition-colors flex items-center gap-0.5 group"
				>
					<ArrowUpRight class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
					Pinterest
				</a>
				<a
					href="https://youtube.com"
					target="_blank"
					rel="noopener noreferrer"
					class="text-black/60 hover:text-black transition-colors flex items-center gap-0.5 group"
				>
					<ArrowUpRight class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
					YouTube
				</a>
			</div>
		</div>
	</div>
</div>

<style>
	label {
		color: var(--color-surface-foreground-muted);
	}
</style>
