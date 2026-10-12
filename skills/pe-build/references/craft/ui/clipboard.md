# Copy confirmation

Copy confirms in the control the reader just used. The label or the icon changes immediately, returns after two seconds, and a polite live region announces the result, including the failure.

`navigator.clipboard.writeText` resolves when the clipboard has the text. It rejects with `NotAllowedError` outside a secure context, without a user gesture, when the document is not focused, or when a permissions policy blocks clipboard write. Call it directly from the click. An `await` ahead of it spends the gesture, and the write then fails.

The button's name stays the action, "Copy". The result is not a new name. A status region mounted from the first render, empty until the click, announces "Copied" or "Copy failed". Inserting that region at the moment of success is announced inconsistently. The visible word, or an icon in its place, is `aria-hidden`. Icon motion belongs to [icon transitions](icon-transitions.md). The live-region rules belong to [screen readers](../../a11y/screen-readers.md).

Do: confirm in place, reset after two seconds, announce through the status region, and catch the rejection.

Don't: leave "Copied" stuck, use `aria-live="assertive"`, or answer a failure with nothing but a console line. The source text stays selectable so the reader can still copy it.

```tsx
import { useEffect, useState } from "react";

const RESET_MS = 2000;

function CopyButton({ value }: { value: string }) {
  const [notice, setNotice] = useState<{ text: string; at: number } | null>(null);

  useEffect(() => {
    if (!notice) return;
    const id = window.setTimeout(() => setNotice(null), RESET_MS);
    return () => window.clearTimeout(id);
  }, [notice]);

  async function onCopy() {
    try {
      await navigator.clipboard.writeText(value);
      setNotice({ text: "Copied", at: Date.now() });
    } catch {
      setNotice({ text: "Copy failed", at: Date.now() });
    }
  }

  return (
    <>
      <button type="button" onClick={onCopy} aria-label="Copy">
        <span aria-hidden="true">{notice?.text ?? "Copy"}</span>
      </button>
      <span role="status" aria-live="polite" className="sr-only">{notice?.text ?? ""}</span>
    </>
  );
}
```

`at` changes on every click, so a second copy restarts the two seconds. `role="status"` is the polite live region. Hide the status visually with the project's [sr-only](../../a11y/screen-readers.md) treatment; do not use `display: none`.

## Verify

Click. The control says "Copied" on that frame, and it says "Copy" again about two seconds later. A second click during the wait restarts the wait. A screen reader announces "Copied" once. On an insecure page, or with clipboard writes blocked, the control says "Copy failed" and the text can still be selected.
