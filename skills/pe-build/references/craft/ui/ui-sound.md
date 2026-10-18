# UI sound

Sound is feedback a user cannot always receive, so it confirms what the screen already shows and never carries information alone.

- Every sound has a visible equivalent, and a setting turns sound off.
- Sound marks rare, meaningful moments (a completed payment, an arriving message). High-frequency interactions (typing, scrolling, hover) stay silent.
- Create one `AudioContext` for the page and reuse it.
- A context created before the user's first gesture starts `suspended`; call `resume()` inside the gesture handler before playing ([Chrome autoplay policy](https://developer.chrome.com/blog/autoplay)).
- Schedule an envelope from a set value: `setValueAtTime` first, then ramp. `exponentialRampToValueAtTime` needs a positive target, so fade to a small value such as `0.0001`, never `0` ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/AudioParam/exponentialRampToValueAtTime)).
- A replayed `<audio>` element sets `currentTime = 0` before `play()`, so a rapid second trigger restarts the sound instead of being dropped.
- Preload short UI sounds; a sound that arrives after its visual change reads as lag.
