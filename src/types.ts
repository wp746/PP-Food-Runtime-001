export type PPFoodMode = "A" | "B";
export type TextMode = "IMAGE_NATIVE" | "HYBRID_COMPOSITE";

export type FactSource = "OBSERVED_FACT" | "USER_VERIFIED_FACT" | "HIGH_CONFIDENCE_INFERENCE" | "UNKNOWN";

export interface UserFacts {
  productName?: string;
  brand?: string;
  headline?: string;
  subtitle?: string;
  slogan?: string;
  sellingPoints?: string[];
  address?: string;
  phone?: string;
  price?: string;
  defaultCopyAuthorized?: boolean;
  layoutTestMode?: boolean;
  textMode?: TextMode;
}

export interface ProductTruth {
  productIdentity: string;
  primaryCategory: string;
  visibleComponents: string[];
  visibleCount?: number | null;
  geometry: string[];
  vesselOrPackage?: Record<string, unknown>;
  platingOrTopology: string[];
  physicalRelationships: string[];
  surfaceState: Record<string, unknown>;
  dominantProductColors: string[];
  sensorySemantics: Record<string, unknown>;
  emotionalSemantics: {
    primary: string[];
    secondary: string[];
    forbidden: string[];
  };
  fidelityRisks: string[];
  unknown: string[];
}

export interface CategoryVisualTranslation {
  primaryCategory: string;
  sensorySemantics: { primary: string[]; secondary: string[] };
  emotionalSemantics: { primary: string[]; secondary: string[]; forbidden: string[] };
  brandTemperament: string[];
  materialMetaphor: { primary: string; secondary?: string };
  typography: {
    personality: string;
    dimensionality: string;
    materialMetaphor: string;
    edgeBehavior: string;
    spatialBehavior: string;
  };
  color: Record<string, unknown>;
  lighting: Record<string, unknown>;
  spatial: Record<string, unknown>;
  motion: Record<string, unknown>;
  information: Record<string, unknown>;
  oneBigIdeaSeed: string;
  forbiddenDrift: string[];
}

export interface ArtDirection {
  conceptId: "PRIMARY" | "CHALLENGER" | string;
  oneBigIdea: string;
  productHeroDirection: string;
  typographyDirection: string;
  typographyProductRelationship: string;
  compositionDirection: string;
  categoryAtmosphere: string;
  colorDirection: string;
  lightingDirection: string;
  forbiddenDrift: string[];
}

export interface GoldenVector {
  productHeroStrength: number;
  headlineAggression: number;
  typographyProductSymbiosis: number;
  oneBigIdeaClarity: number;
  compositionalDepthTension: number;
  categoryInevitability: number;
  informationDensityControl: number;
  commercialFinish: number;
}

export type EvaluationDecision = "PASS" | "RETRY" | "NO_QUALIFIED_WINNER" | "NEEDS_HUMAN_REVIEW" | "PROVIDER_FAILURE";

export interface EvaluationResult {
  decision: EvaluationDecision;
  failures: Array<{ code: string; severity: "CRITICAL" | "MAJOR" | "MINOR"; evidence: string[] }>;
  firstRead?: [string?, string?, string?];
  goldenVector?: GoldenVector;
  passFreeze?: Record<string, boolean>;
}

export interface PPFoodJobInput extends UserFacts {
  jobId: string;
  mode: PPFoodMode;
  sourceImage: string | Buffer;
  stageAPassImage?: string | Buffer;
  aspectRatio?: "9:16";
}

export interface ImageProviderResult {
  image: Buffer | string;
  provider: string;
  model: string;
  requestId?: string;
}

export interface ImageProvider {
  edit(input: {
    image: Buffer | string;
    prompt: string;
    aspectRatio: "9:16";
  }): Promise<ImageProviderResult>;
}

export interface VisionProvider {
  analyze<T = unknown>(input: {
    system: string;
    images: Array<Buffer | string>;
    input?: unknown;
    responseFormat?: "json" | "text";
  }): Promise<T>;
}

export interface TextProvider {
  complete<T = unknown>(input: {
    system: string;
    input: unknown;
    responseFormat?: "json" | "text";
  }): Promise<T>;
}
