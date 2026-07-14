import { browser } from '$app/environment';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

if (browser) {
    gsap.registerPlugin(ScrollTrigger);
}

type GSAPTween = gsap.core.Tween;

// Narrowed from `keyof typeof gsap` to the methods that actually match this
// call signature (single vars object). `fromTo` isn't included because it
// needs two vars objects (from + to) and never worked with this signature —
// so this isn't a behavior change, just more accurate typing.
type AnimationMethod = 'to' | 'from' | 'set';

interface AnimationStep extends GSAPTweenVars {
	type: AnimationMethod;
	scrollTrigger?: ScrollTrigger.Vars;
}

// Backward compatible: pass a single step (old behavior, unchanged) or an
// array of steps to run in sequence, each starting only once the previous
// one completes.
type AnimationOptions = AnimationStep | AnimationStep[];

export function animate(node: HTMLElement, options: AnimationOptions): { destroy?: () => void } {
	const steps: AnimationStep[] = Array.isArray(options) ? options : [options];

	const createdTweens: GSAPTween[] = [];
	const createdTriggers: ScrollTrigger[] = [];
	let cancelled = false;

	function runStep(index: number) {
		if (cancelled || index >= steps.length) return;

		const { type, scrollTrigger, ...vars } = steps[index];
		const method = gsap[type] as
			((target: gsap.TweenTarget, vars: GSAPTweenVars) => GSAPTween) | undefined;

		if (!method) {
			console.warn(`GSAP method "${type}" does not exist.`);
			runStep(index + 1);
			return;
		}

		const isLastStep = index === steps.length - 1;
		const userOnComplete = vars.onComplete;

		const tween = method(node, {
			...vars,
			scrollTrigger: scrollTrigger
				? { ...scrollTrigger, trigger: scrollTrigger.trigger || node }
				: undefined,
			onComplete: () => {
				userOnComplete?.();
				if (!isLastStep) {
					requestAnimationFrame(() => {
						ScrollTrigger.refresh();
						runStep(index + 1);
					});
				}
			}
		});

		createdTweens.push(tween);
		if (tween.scrollTrigger) createdTriggers.push(tween.scrollTrigger);
	}

	runStep(0);

	return {
		destroy() {
			// Prevents a not-yet-created later step from starting if the
			// element is torn down mid-sequence
			cancelled = true;
			createdTweens.forEach((t) => t.kill());
			createdTriggers.forEach((st) => st.kill());
		}
	};
}
