import { ImageItem } from "../types";

export const SAMPLE_IMAGES: ImageItem[] = [
  {
    id: "sample-1",
    name: "hero-banner-large.jpg",
    path: "/uploads/2026/08/hero-banner-large.jpg",
    originalSizeBytes: 1850000, // 1.85 MB (>400KB threshold)
    width: 3840,
    height: 2160,
    format: "JPEG",
    previewUrl: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop&q=80",
    status: "pending"
  },
  {
    id: "sample-2",
    name: "product-showcase.png",
    path: "/uploads/products/product-showcase.png",
    originalSizeBytes: 920000, // 920 KB
    width: 2400,
    height: 1600,
    format: "PNG",
    previewUrl: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
    status: "pending"
  },
  {
    id: "sample-3",
    name: "small-icon.png",
    path: "/uploads/assets/small-icon.png",
    originalSizeBytes: 180000, // 180 KB (<400KB threshold)
    width: 512,
    height: 512,
    format: "PNG",
    previewUrl: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=80",
    status: "pending"
  },
  {
    id: "sample-4",
    name: "landscape-photography.tif",
    path: "/gallery/2026/landscape-photography.tif",
    originalSizeBytes: 4800000, // 4.8 MB
    width: 4096,
    height: 2730,
    format: "TIFF",
    previewUrl: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&auto=format&fit=crop&q=80",
    status: "pending"
  }
];
