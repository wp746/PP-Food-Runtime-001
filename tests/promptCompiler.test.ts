import { describe, expect, it } from "vitest";
import { compileStageAPrompt, compileStageBPrompt } from "../src/ppFoodPrompts";
import type { ArtDirection, ProductTruth } from "../src/types";

const productTruth: ProductTruth = {
  productIdentity: "碱水原味贝果",
  primaryCategory: "BAKERY",
  visibleComponents: ["贝果"],
  visibleCount: 3,
  geometry: ["round ring bread"],
  platingOrTopology: ["three bagels grouped together"],
  physicalRelationships: [],
  surfaceState: { crust: "deep amber baked crust", gloss: "moderate" },
  dominantProductColors: ["amber", "brown"],
  sensorySemantics: { baked: true, grain: true, chewiness: "high" },
  emotionalSemantics: { primary: ["warm", "crafted"], secondary: [], forbidden: [] },
  fidelityRisks: [],
  unknown: []
};

const direction: ArtDirection = {
  conceptId: "PRIMARY",
  oneBigIdea: "Turn baked grain warmth and chewy crust into a contemporary tactile campaign world.",
  productHeroDirection: "Large close product hero in the lower-mid foreground.",
  typographyDirection: "Embossed toasted-grain headline with controlled warm dimensionality.",
  typographyProductRelationship: "Share grazing light, baked-edge material logic and perspective.",
  compositionDirection: "Asymmetric multi-depth composition with overlap and foreground pressure.",
  categoryAtmosphere: "Warm modern bakery atmosphere without literal oven/tunnel clichés.",
  colorDirection: "Cream, amber and deep brown support palette.",
  lightingDirection: "Warm grazing key plus amber edge separation.",
  forbiddenDrift: ["wooden sign", "oven tunnel"]
};

describe("PP Food prompt compiler", () => {
  it("Stage A forbids poster text and preserves product truth", () => {
    const prompt = compileStageAPrompt({
      productTruth,
      artDirection: {
        backgroundDirection: "Modern warm bakery environment with controlled depth.",
        lightingDirection: "Warm grazing key light.",
        compositionDirection: "Close hero framing."
      }
    });

    expect(prompt).toContain("No poster layout");
    expect(prompt).toContain("Do not MUTATE");
    expect(prompt).toContain("BAKERY");
  });

  it("Stage B contains product-hero/headline-hero hierarchy and anti-template rules", () => {
    const prompt = compileStageBPrompt({
      productTruth,
      userFacts: {
        productName: "碱水原味贝果",
        headline: "碱水原味贝果",
        subtitle: "现烤出炉，越嚼越香",
        brand: "欧丰园",
        defaultCopyAuthorized: true
      },
      direction
    });

    expect(prompt).toContain("The product is visual hero #1");
    expect(prompt).toContain("The headline is visual hero #2");
    expect(prompt).toContain("No giant literal noun-based environment");
    expect(prompt).toContain("碱水原味贝果");
  });
});
