import type {
  ArtDirection,
  CategoryVisualTranslation,
  EvaluationResult,
  ImageProvider,
  PPFoodJobInput,
  ProductTruth,
  TextProvider,
  VisionProvider,
} from "./types";
import {
  B_ART_DIRECTOR_SYSTEM,
  B_EVALUATOR_SYSTEM,
  CATEGORY_TRANSLATOR_SYSTEM,
  COPY_FIREWALL_SYSTEM,
  RETRY_PLANNER_SYSTEM,
  STAGE_A_DIRECTOR_SYSTEM,
  STAGE_A_QC_SYSTEM,
  VISION_OBSERVER_SYSTEM,
  compileStageAPrompt,
  compileStageBPrompt,
} from "./ppFoodPrompts";

export class PPFoodPipeline {
  constructor(
    private readonly vision: VisionProvider,
    private readonly text: TextProvider,
    private readonly image: ImageProvider,
  ) {}

  async analyzeSource(sourceImage: string | Buffer): Promise<ProductTruth> {
    return this.vision.analyze<ProductTruth>({
      system: VISION_OBSERVER_SYSTEM,
      images: [sourceImage],
      responseFormat: "json",
    });
  }

  async runStageA(job: PPFoodJobInput): Promise<{
    productTruth: ProductTruth;
    prompt: string;
    image: Awaited<ReturnType<ImageProvider["edit"]>>;
    qc: EvaluationResult;
  }> {
    const productTruth = await this.analyzeSource(job.sourceImage);

    const artDirection = await this.text.complete<{
      backgroundDirection: string;
      lightingDirection: string;
      compositionDirection: string;
      commercialDirection?: string;
    }>({
      system: STAGE_A_DIRECTOR_SYSTEM,
      input: { productTruth, userFacts: job },
      responseFormat: "json",
    });

    const prompt = compileStageAPrompt({
      productTruth,
      productName: job.productName,
      artDirection,
    });

    const rendered = await this.image.edit({
      image: job.sourceImage,
      prompt,
      aspectRatio: "9:16",
    });

    const qc = await this.vision.analyze<EvaluationResult>({
      system: STAGE_A_QC_SYSTEM,
      images: [job.sourceImage, rendered.image],
      input: { productTruth, promptVersion: "handoff-v1" },
      responseFormat: "json",
    });

    return { productTruth, prompt, image: rendered, qc };
  }

  async runStageB(job: PPFoodJobInput, productTruth?: ProductTruth): Promise<{
    productTruth: ProductTruth;
    copyAllowlist: unknown;
    translation: CategoryVisualTranslation;
    primary: { direction: ArtDirection; prompt: string; image: Awaited<ReturnType<ImageProvider["edit"]>> };
    challenger: { direction: ArtDirection; prompt: string; image: Awaited<ReturnType<ImageProvider["edit"]>> };
    evaluation: EvaluationResult;
  }> {
    if (!job.stageAPassImage) {
      throw new Error("Stage B requires the current job Stage A PASS image.");
    }

    const truth = productTruth ?? (await this.analyzeSource(job.sourceImage));

    const copyAllowlist = await this.text.complete({
      system: COPY_FIREWALL_SYSTEM,
      input: {
        productTruth: truth,
        userFacts: job,
      },
      responseFormat: "json",
    });

    const translation = await this.text.complete<CategoryVisualTranslation>({
      system: CATEGORY_TRANSLATOR_SYSTEM,
      input: {
        productTruth: truth,
        userFacts: job,
        copyAllowlist,
      },
      responseFormat: "json",
    });

    const primaryDirection = await this.text.complete<ArtDirection>({
      system: B_ART_DIRECTOR_SYSTEM,
      input: {
        variant: "PRIMARY",
        productTruth: truth,
        userFacts: job,
        copyAllowlist,
        translation,
      },
      responseFormat: "json",
    });

    const challengerDirection = await this.text.complete<ArtDirection>({
      system: B_ART_DIRECTOR_SYSTEM,
      input: {
        variant: "CHALLENGER",
        diversityRequirement:
          "Must differ from Primary in at least two structural dimensions: composition axis, headline spatial behavior, product placement, energy direction, depth architecture, information integration.",
        productTruth: truth,
        userFacts: job,
        copyAllowlist,
        translation,
        primaryDirection,
      },
      responseFormat: "json",
    });

    const primaryPrompt = compileStageBPrompt({
      productTruth: truth,
      userFacts: job,
      direction: primaryDirection,
      brandTemperament: translation.brandTemperament,
    });

    const challengerPrompt = compileStageBPrompt({
      productTruth: truth,
      userFacts: job,
      direction: challengerDirection,
      brandTemperament: translation.brandTemperament,
    });

    const [primaryImage, challengerImage] = await Promise.all([
      this.image.edit({ image: job.stageAPassImage, prompt: primaryPrompt, aspectRatio: "9:16" }),
      this.image.edit({ image: job.stageAPassImage, prompt: challengerPrompt, aspectRatio: "9:16" }),
    ]);

    const evaluation = await this.vision.analyze<EvaluationResult>({
      system: B_EVALUATOR_SYSTEM,
      images: [job.sourceImage, job.stageAPassImage, primaryImage.image, challengerImage.image],
      input: {
        productTruth: truth,
        userFacts: job,
        copyAllowlist,
        translation,
        primaryDirection,
        challengerDirection,
      },
      responseFormat: "json",
    });

    return {
      productTruth: truth,
      copyAllowlist,
      translation,
      primary: { direction: primaryDirection, prompt: primaryPrompt, image: primaryImage },
      challenger: { direction: challengerDirection, prompt: challengerPrompt, image: challengerImage },
      evaluation,
    };
  }

  async planRetry(input: unknown) {
    return this.text.complete({
      system: RETRY_PLANNER_SYSTEM,
      input,
      responseFormat: "json",
    });
  }
}
