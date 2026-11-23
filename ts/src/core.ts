export class SpendCapError extends Error {}

/** Fold case and compatibility forms, then collapse whitespace. Idempotent. */
export function normalise(text: string): string {
  let folded = text.normalize("NFKD").toLowerCase();
  folded = folded.normalize("NFKD").toLowerCase().normalize("NFKD");
  return folded.split(/\s+/u).filter(Boolean).join(" ");
}

/** Return the new total, or throw before the cap is passed. */
export function checkSpend(spentUsd: number, nextCostUsd: number, capUsd: number): number {
  if (spentUsd < 0 || nextCostUsd < 0 || capUsd < 0) {
    throw new RangeError("amounts must not be negative");
  }
  const total = spentUsd + nextCostUsd;
  if (total > capUsd) {
    throw new SpendCapError(`spend ${total.toFixed(2)} would pass cap ${capUsd.toFixed(2)}`);
  }
  return total;
}
