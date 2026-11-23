import { describe, expect, it } from "vitest";
import { SpendCapError, checkSpend, normalise } from "../src/core.js";
import { demo } from "../src/demo.js";

describe("normalise", () => {
  it("collapses whitespace and case", () => {
    expect(normalise("  Hello   WORLD \n")).toBe("hello world");
  });
  it("is idempotent on samples", () => {
    for (const s of ["", "ÀB  c", "ｆｕｌｌ　ｗｉｄｔｈ", "a\tb"]) {
      expect(normalise(normalise(s))).toBe(normalise(s));
    }
  });
});

describe("checkSpend", () => {
  it("allows spend at the cap", () => {
    expect(checkSpend(0.25, 0.25, 0.5)).toBeCloseTo(0.5);
  });
  it("refuses spend above the cap", () => {
    expect(() => checkSpend(0.25, 0.26, 0.5)).toThrow(SpendCapError);
  });
  it("refuses negative amounts", () => {
    expect(() => checkSpend(-1, 0, 1)).toThrow("amounts must not be negative");
  });
  it("allows zeros", () => {
    expect(checkSpend(0, 0, 0)).toBe(0);
  });
});

describe("demo", () => {
  it("prints the expected lines", () => {
    expect(demo()).toEqual(["hello world", "total spend: 0.15"]);
  });
});
