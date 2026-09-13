"use strict";

/**
 * Coalesce equal polling cadences into one native browser interval.
 *
 * Dashboard modules historically created many independent 1s/3s/5s timers.
 * They remain source-compatible, but callbacks with the same cadence now share
 * one scheduler, are staggered by a few milliseconds, and are throttled while
 * the document is hidden. This reduces simultaneous HTTP bursts and browser /
 * ThreadingHTTPServer context switching without changing API payloads.
 */
export function installPollingGovernor() {
  if (window.__mhrnPollingGovernorInstalled) return;
  window.__mhrnPollingGovernorInstalled = true;

  const nativeSetInterval = window.setInterval.bind(window);
  const nativeClearInterval = window.clearInterval.bind(window);
  const nativeSetTimeout = window.setTimeout.bind(window);
  const buckets = new Map();
  const handles = new Map();
  let nextHandle = 1_000_000_000;

  function tickBucket(bucket) {
    bucket.cycles += 1;
    if (document.hidden && bucket.cycles % 4 !== 0) return;
    const callbacks = [...bucket.callbacks.values()];
    callbacks.forEach((entry, index) => {
      nativeSetTimeout(() => {
        try {
          entry.callback(...entry.args);
        } catch (error) {
          console.error("polling callback failed", error);
        }
      }, index * 25);
    });
  }

  window.setInterval = function governedSetInterval(callback, delay = 0, ...args) {
    if (typeof callback !== "function") {
      return nativeSetInterval(callback, delay, ...args);
    }
    const cadence = Math.max(250, Math.trunc(Number(delay) || 0));
    let bucket = buckets.get(cadence);
    if (!bucket) {
      bucket = { callbacks: new Map(), nativeId: null, cycles: 0 };
      bucket.nativeId = nativeSetInterval(() => tickBucket(bucket), cadence);
      buckets.set(cadence, bucket);
    }
    const handle = nextHandle++;
    bucket.callbacks.set(handle, { callback, args });
    handles.set(handle, cadence);
    return handle;
  };

  window.clearInterval = function governedClearInterval(handle) {
    const cadence = handles.get(handle);
    if (cadence === undefined) {
      nativeClearInterval(handle);
      return;
    }
    handles.delete(handle);
    const bucket = buckets.get(cadence);
    if (!bucket) return;
    bucket.callbacks.delete(handle);
    if (!bucket.callbacks.size) {
      nativeClearInterval(bucket.nativeId);
      buckets.delete(cadence);
    }
  };

  window.MHRNPollingGovernor = {
    stats() {
      return {
        nativeIntervals: buckets.size,
        logicalIntervals: handles.size,
        hidden: document.hidden,
      };
    },
  };
}
