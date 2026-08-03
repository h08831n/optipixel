export type TargetFormat = "WEBP" | "AVIF" | "JPEG" | "PNG" | "TIFF" | "BMP" | "ORIGINAL";

export type OutputMode = "folder" | "replace" | "next_to_original";

export type LanguageCode = "en" | "fa" | "de" | "tr" | "ar" | "fr" | "es" | "ru";

export interface ImageItem {
  id: string;
  name: string;
  path: string;
  originalSizeBytes: number;
  width: number;
  height: number;
  format: string;
  dataUrl?: string;
  previewUrl?: string;
  status: "pending" | "processing" | "optimized" | "converted" | "skipped" | "failed";
  optimizedSizeBytes?: number;
  optimizedFormat?: TargetFormat;
  reductionPercentage?: number;
  savedBytes?: number;
  message?: string;
  durationMs?: number;
  optimizedDataUrl?: string;
}

export interface ProcessingSettings {
  targetFormat: TargetFormat;
  quality: number; // 1-100
  webpMode: "lossy" | "lossless";
  thresholdEnabled: boolean;
  sizeThresholdKb: number;
  keepOriginalIfLarger: boolean;
  enableResize: boolean;
  maxWidth: number;
  maxHeight: number;
  keepAspectRatio: boolean;
  onlyShrink: boolean;
  stripMetadata: boolean;
  outputMode: OutputMode;
  outputFolder: string;
  preserveStructure: boolean;
  createBackup: boolean;
  workers: number;
}

export interface JobHistoryEntry {
  id: number;
  timestamp: string;
  operation: string;
  filesProcessed: number;
  savedBytes: number;
  durationSeconds: number;
}
