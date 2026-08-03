<script lang="ts">
    import { animate } from '$lib/utils/animate';

    let { text, image }: { text: string; image: string } = $props();

    const words = $derived(text.trim().split(/\s+/));
</script>

<div class="h-88 sm:h-104 md:h-120 relative w-full overflow-hidden bg-background">
    <div class="h-full w-full">
        <img
            src={image}
            alt={text}
            loading='eager'
            class="h-full w-full object-cover will-change-transform"
            use:animate={[
                {
                    type: 'to',
                    scale: 1.5,

                    ease: 'none',
                    scrollTrigger: {
                        start: 'top bottom',
                        end: 'bottom top',

                        scrub: 1
                    }
                }
            ]}
        />
    </div>

    <!-- Left-to-right text background scrim -->
    <div
        class="h-full absolute top-0 left-0 w-full bg-linear-to-r from-black/80 via-black/40 to-transparent flex items-end p-6 sm:p-12 md:p-20"
    >
        <p class="font-display text-2xl sm:text-4xl md:text-5xl text-white leading-tight sm:leading-snug md:leading-15 w-full sm:w-2/3 md:w-1/2 lg:w-1/3">
            {#each words as word, index (word + index)}
                <span
                    class="inline-block will-change-transform"
                    use:animate={[
                        {
                            type: 'from',
                            y: 40,
                            x: 20,
                            opacity: 0,
                            filter: 'blur(6px)',
                            duration: 1,
                            delay: index * 0.045,
                            ease: 'power4.out'
                        }
                    ]}
                >
                    {word}
                </span>{index < words.length - 1 ? ' ' : ''}
            {/each}
        </p>
    </div>

    <!-- Eased bottom fade container -->
</div>