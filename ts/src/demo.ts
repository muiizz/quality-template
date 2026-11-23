import { checkSpend, normalise } from "./core.js";

export function demo(): string[] {
  return [normalise("  Hello   WORLD  "), `total spend: ${checkSpend(0.1, 0.05, 0.5).toFixed(2)}`];
}
