<script lang="ts">
    import { enhance } from '$app/forms';
    import { fade, fly } from 'svelte/transition';
    import AnimatedPillGroup from '$lib/components/ui/animated-pill/animated-pill-group.svelte';
    import AnimatedPillItem from '$lib/components/ui/animated-pill/animated-pill-item.svelte';
    import { Button } from '$lib/components/ui/button';
    import * as Dialog from '$lib/components/ui/dialog';
    import Input from '$lib/components/ui/input.svelte';
    import ArrowRight from '@tabler/icons-svelte-runes/icons/arrow-right';
    import ArrowUpRight from '@tabler/icons-svelte-runes/icons/arrow-up-right';
    import {PUBLIC_BACKEND_URL} from "$env/static/public"

    let { data } = $props();

    const categories = $state([
        { name: 'All', href: '/catalog' },
        { name: 'Mixed Media', href: '/catalog/mixed-media' },
        { name: 'Landscapes', href: '/catalog/landscapes' },
        { name: 'Portraits', href: '/catalog/portraits' }
    ]);

    let catalog = $derived(data.catalog ?? []);
    let selectedCategory = $state('All');

    // Filtered view according to selected category pill
    let filteredCatalog = $derived(
        selectedCategory === 'All'
            ? catalog
            : catalog.filter((item) => item.category === selectedCategory)
    );

    // Reactive state maps per artwork index
    let formData = $state<Record<number, { fullName: string; email: string; countryCode: string; phone: string; message: string }>>({});
    let submitted = $state<Record<number, boolean>>({});
    let attemptedSubmit = $state<Record<number, boolean>>({});
    let loading = $state<Record<number, boolean>>({});

    function getFormState(index: number) {
        return formData[index] ?? { fullName: '', email: '', countryCode: '+250', phone: '', message: '' };
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
        return (
            form.fullName.trim().length > 0 &&
            /^\S+@\S+\.\S+$/.test(form.email)
        );
    }
</script>

<svelte:head>
    <title>Catalog</title>
</svelte:head>

<div class="h-[30dvh] bg-surface w-full flex flex-col justify-end px-6 sm:px-12 md:px-20">
    <div class="py-10">
        <p class="font-display text-3xl sm:text-4xl md:text-5xl">Artwork by David</p>
    </div>
</div>

<div class="px-6 sm:px-12 md:px-20 py-10 md:py-20 flex flex-col space-y-10 md:space-y-20 bg-background">
    <div class="flex items-center justify-between w-full overflow-x-auto pb-2 md:pb-0">
        <div class="bg-surface rounded-full p-2 border w-fit border-black/20 shrink-0">
            <AnimatedPillGroup color="var(--color-foreground)" direction="horizontal">
                {#each categories as category (category.name)}
                    <AnimatedPillItem
                        class={`py-2 px-4 text-sm hover:text-white ${category.name === selectedCategory ? ' text-white' : ''}`}
                        active={category.name === selectedCategory}
                        onclick={() => (selectedCategory = category.name)}
                    >
                        <p>{category.name}</p>
                    </AnimatedPillItem>
                {/each}
            </AnimatedPillGroup>
        </div>
    </div>

    <div class="p-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12 md:gap-y-20">
        {#each filteredCatalog as artwork, index (artwork.catalog_id ?? artwork.name)}
            {@const form = getFormState(index)}
            <div
                class={`space-y-6 pb-10 ${index < filteredCatalog.length - 1 ? 'border-b md:border-b-0 border-black/30' : ''} ${index < filteredCatalog.length - (filteredCatalog.length % 3 || 3) ? 'md:border-b md:border-black/30' : ''}`}
            >
                <img
                    src={`${PUBLIC_BACKEND_URL}/${artwork.image}`}
                    alt={artwork.name}
                    class="h-[25rem] sm:h-[30rem] md:h-[35rem] w-full object-cover rounded-2xl"
                />
                <div>
                    <p class="font-display font-semibold text-xl">{artwork.name}</p>
                    <div class="py-4 space-y-2 text-surface-foreground-muted">
                        <p>{artwork.category || 'Uncategorized'}</p>
                        <p>{artwork.dimensions || 'Variable'}</p>
                    </div>

                    <div class="flex items-center justify-between">
                        <p class="font-semibold">USD {artwork.price}</p>

                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button color="black" variant="tonal" size="sm">
                                    Inquire <ArrowRight class="ml-1 w-4 h-4" />
                                </Button>
                            </Dialog.Trigger>

                            <Dialog.Content
                                class="z-[60] fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-h-[85dvh] h-[90dvh] md:h-[75%] min-w-[95%] md:min-w-[90%] grid grid-cols-1 md:grid-cols-5 gap-4 p-0 overflow-y-auto md:overflow-hidden bg-transparent rounded-3xl"
                            >
                                <!-- Left Column: Artwork Specs & Preview -->
                                <div class="md:col-span-3 bg-surface overflow-y-auto p-6 md:p-8 space-y-6 min-h-[250px] md:min-h-0">
                                    <div class="relative w-full h-full min-h-[250px] overflow-hidden">
                                        <img
                                            src={`${PUBLIC_BACKEND_URL}/${artwork.image}`}
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
                                                Thank you for your interest in <span class="font-semibold text-foreground">"{artwork.name}"</span>. We will follow up with you by email shortly.
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
                                                            oninput={(e: Event) => updateFormField(index, 'fullName', (e.target as HTMLInputElement).value)}
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
                                                            oninput={(e: Event) => updateFormField(index, 'email', (e.target as HTMLInputElement).value)}
                                                        />
                                                        {#if attemptedSubmit[index] && !/^\S+@\S+\.\S+$/.test(form.email)}
                                                            <p class="text-xs text-red-600">A valid email is required.</p>
                                                        {/if}
                                                    </div>
                                                </div>

                                                <div class="flex gap-1 items-end">
                                                    <div class="flex flex-col w-20 space-y-2">
                                                        <label for={`phone-code-${index}`} class="text-nowrap text-sm font-semibold">Code</label>
                                                        <Input
                                                            context="surface"
                                                            placeholder="+250"
                                                            value={form.countryCode}
                                                            oninput={(e: Event) => updateFormField(index, 'countryCode', (e.target as HTMLInputElement).value)}
                                                            inputmode="tel"
                                                            maxlength={6}
                                                            class="rounded-r-none text-nowrap"
                                                            id={`phone-code-${index}`}
                                                        />
                                                    </div>
                                                    <div class="flex-1 space-y-2">
                                                        <label for={`phone-${index}`} class="text-nowrap text-sm font-semibold">Phone number</label>
                                                        <Input
                                                            context="surface"
                                                            placeholder="788 000 000"
                                                            value={form.phone}
                                                            oninput={(e: Event) => updateFormField(index, 'phone', (e.target as HTMLInputElement).value)}
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
                                                    <label for={`message-${index}`} class="text-sm font-semibold">Message / Questions</label>
                                                    <textarea
                                                        id={`message-${index}`}
                                                        name="message"
                                                        rows="3"
                                                        placeholder="Ask about shipping, framing, or custom arrangements..."
                                                        value={form.message}
                                                        oninput={(e: Event) => updateFormField(index, 'message', (e.target as HTMLTextAreaElement).value)}
                                                        class="w-full bg-background border border-black/10 rounded-2xl p-4 text-sm focus:outline-hidden focus:border-black transition-colors resize-none"
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
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>

<div class="px-6 md:px-10 py-12 md:py-20 border-t border-black/10 bg-foreground text-white">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between lg:justify-evenly gap-8 md:gap-0">
        <div class="space-y-4 md:space-y-6">
            <p class="text-2xl sm:text-3xl md:text-4xl font-display font-medium">Don't see what you're looking for?</p>
            <p class="text-nav-foreground-muted text-sm">
                Studio Mugire accepts a limited number of commissions each year. <br class="hidden sm:block" /> Reach out to discuss a
                custom work made specifically for your space.
            </p>
        </div>

        <Button color="white" size="lg" class="w-full md:w-auto">REQUEST A COMMISSION</Button>
    </div>
</div>