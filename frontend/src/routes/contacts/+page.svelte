<script lang="ts">
    import { enhance } from '$app/forms';
    import { fade, fly } from 'svelte/transition';
    import PageBanner from '$lib/components/page-banner.svelte';
    import Mail from '@tabler/icons-svelte-runes/icons/mail';
    import Phone from '@tabler/icons-svelte-runes/icons/phone';
    import MapPin from '@tabler/icons-svelte-runes/icons/map-pin';
    import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';

    // Form states using Svelte 5 runes
    let name = $state('');
    let email = $state('');
    let phone = $state('');
    let message = $state('');

    let loading = $state(false);
    let submitted = $state(false);
    let errorMessage = $state('');
</script>

<PageBanner text="Bring Your Vision To The Canvas." image="/contact4.jpg" />

<div class="px-6 sm:px-12 md:px-20 py-16 md:py-24 max-w-7xl mx-auto flex flex-col lg:flex-row items-start justify-between gap-12 lg:gap-20">
    <!-- Left Column: Artistic Copy & Quick Direct Info -->
    <div class="w-full lg:w-1/2 lg:sticky lg:top-12">
        <div class="space-y-6 pb-12">
            <span class="inline-block text-xs uppercase tracking-widest font-semibold text-surface-foreground-muted/80">
                Connect with the Studio
            </span>
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-display font-light text-foreground leading-[1.1] tracking-tight">
                Let’s co-create <br class="hidden sm:inline" /> something

                <span class="relative inline-block italic font-normal text-foreground/70">
                    permanent
                    <svg
                        class="ink-underline absolute -bottom-2 left-0 w-full overflow-visible"
                        viewBox="0 0 160 12"
                        preserveAspectRatio="none"
                        aria-hidden="true"
                    >
                        <path
                            d="M2 8.5 C 30 3, 60 10, 88 5 S 140 2, 158 6"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            class="text-surface-foreground-muted/40"
                        />
                    </svg>
                </span>
            </h1>
            <p class="text-surface-foreground-muted text-base md:text-lg font-light max-w-md leading-relaxed pt-2">
                Whether you're looking to acquire an original piece, enroll in a masterclass, or commission custom work—our doors are open.
            </p>
        </div>

        <!-- Direct Contact Quick List -->
        <div class="border-t border-surface-border/60 pt-10 space-y-8">
            <div class="flex items-start gap-4 group cursor-pointer">
                <div
                    class="p-3 rounded-2xl bg-surface-border/30 text-foreground group-hover:bg-foreground group-hover:text-surface transition-all duration-300 group-hover:scale-105"
                >
                    <Mail class="w-5 h-5" />
                </div>
                <div>
                    <h4 class="text-[10px] uppercase tracking-widest text-surface-foreground-muted font-semibold">Inquiries</h4>
                    <a
                        href="mailto:studio@mugire.com"
                        class="text-sm md:text-base font-medium text-foreground hover:opacity-70 transition-opacity"
                    >
                        studio@mugire.com
                    </a>
                </div>
            </div>

            <div class="flex items-start gap-4 group cursor-pointer">
                <div
                    class="p-3 rounded-2xl bg-surface-border/30 text-foreground group-hover:bg-foreground group-hover:text-surface transition-all duration-300 group-hover:scale-105"
                >
                    <Phone class="w-5 h-5" />
                </div>
                <div>
                    <h4 class="text-[10px] uppercase tracking-widest text-surface-foreground-muted font-semibold">
                        Call the Atelier
                    </h4>
                    <a 
                        href="tel:+1234567890" 
                        class="text-sm md:text-base font-medium text-foreground hover:opacity-70 transition-opacity"
                    >
                        +1 (234) 567-890
                    </a>
                </div>
            </div>

            <div class="flex items-start gap-4 group">
                <div
                    class="p-3 rounded-2xl bg-surface-border/30 text-foreground group-hover:bg-foreground group-hover:text-surface transition-all duration-300 group-hover:scale-105"
                >
                    <MapPin class="w-5 h-5" />
                </div>
                <div>
                    <h4 class="text-[10px] uppercase tracking-widest text-surface-foreground-muted font-semibold">Visit Us</h4>
                    <p class="text-sm md:text-base text-foreground/80 leading-snug">
                        104 Beaux-Arts Blvd, Suite 400<br />Paris, NY 10013
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- Right Column: Elevated Atelier Form -->
    <div class="w-full lg:w-1/2 xl:w-5/12">
        <div class="bg-transparent rounded-3xl p-8 sm:p-10 transition-all duration-500 hover:border-surface-border">
            {#if submitted}
                <div in:fly={{ y: 20, duration: 400 }} out:fade={{ duration: 200 }} class="py-12 text-center space-y-6">
                    <div class="w-12 h-12 rounded-full bg-foreground/5 text-foreground mx-auto flex items-center justify-center">
                        <ArrowUpRight class="w-6 h-6" />
                    </div>
                    <div class="space-y-2">
                        <h3 class="font-display font-light text-3xl text-foreground">Inquiry Received</h3>
                        <p class="text-surface-foreground-muted text-sm leading-relaxed max-w-xs mx-auto">
                            Thank you for reaching out. We have received your message and will respond within 24 hours.
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
                                    (result.data?.error as string) ||
                                    'An error occurred while sending your inquiry.';
                            }
                        };
                    }}
                >
                    {#if errorMessage}
                        <div in:fly={{ y: -10, duration: 200 }} class="p-4 bg-red-500/10 text-red-600 text-xs rounded-xl border border-red-500/20 font-medium">
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
                            <span class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"></span>
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
                            <span class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"></span>
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
                        <span class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"></span>
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
                        <span class="absolute bottom-0 left-0 h-[1.5px] w-0 bg-foreground transition-all duration-300 peer-focus:w-full"></span>
                    </div>

                    <!-- Submit Button -->
                    <div class="pt-4 flex justify-end">
                        <button
                            type="submit"
                            disabled={loading}
                            class="w-full sm:w-auto bg-foreground hover:opacity-90 disabled:opacity-50 text-surface text-xs tracking-widest uppercase font-medium py-4 px-9 rounded-full flex items-center justify-center gap-3 group transition-all duration-300 shadow-md hover:shadow-xl cursor-pointer"
                        >
                            <span>{loading ? 'Sending...' : 'Send Inquiry'}</span>
                            <ArrowUpRight
                                class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
                            />
                        </button>
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
                {#each ['Instagram', 'Pinterest', 'YouTube'] as platform (platform)}
                    <a
                        href="https://{platform.toLowerCase()}.com"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-foreground/70 hover:text-foreground transition-colors flex items-center gap-1 group py-1"
                    >
                        <span>{platform}</span>
                        <ArrowUpRight class="w-3.5 h-3.5 opacity-40 group-hover:opacity-100 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                    </a>
                {/each}
            </div>
        </div>
    </div>
</div>