import { useEffect, useSyncExternalStore } from 'react';
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';

/** Smooth scrolling on the start page, never under reduced motion; removed when the page leaves. */
export function useLenis(enabled: boolean) {
  useEffect(() => {
    if (!enabled) return;
    const lenis = new Lenis({ autoRaf: true, lerp: 0.1 });
    return () => lenis.destroy();
  }, [enabled]);
}

const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)');

/** True while the visitor asks for less motion; follows the setting if it changes. */
export function usePrefersReducedMotion() {
  return useSyncExternalStore(changed => {
    const query = reducedMotion();
    query.addEventListener('change', changed);
    return () => query.removeEventListener('change', changed);
  }, () => reducedMotion().matches, () => false);
}
