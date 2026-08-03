import React from "react";
import { LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { RefreshCw, ArrowRight, CheckCircle2 } from "lucide-react";

interface ConvertPageProps {
  lang: LanguageCode;
}

export const ConvertPage: React.FC<ConvertPageProps> = ({ lang }) => {
  const t: TranslationSchema = translations[lang] || translations.en;

  const conversions = [
    { from: "JPEG / JPG", to: "WebP", desc: "Reduces size by ~40-60% for modern websites", lossy: true },
    { from: "PNG", to: "WebP", desc: "Preserves alpha transparency with smaller footprint", lossy: true },
    { from: "JPEG / PNG", to: "AVIF", desc: "Next-gen codec offering maximum compression ratio", lossy: true },
    { from: "HEIC / HEIF", to: "WebP", desc: "Converts iPhone/Apple photos for cross-platform web use", lossy: false },
    { from: "WebP", to: "JPEG", desc: "Converts modern WebP back for legacy desktop software", lossy: false },
    { from: "WebP", to: "PNG", desc: "Unpacks WebP graphics into standard raster PNG", lossy: false }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center space-x-3 rtl:space-x-reverse mb-2">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
            <RefreshCw className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Batch Format Converter Matrix</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">High-performance ImageMagick CLI batch conversion engine</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {conversions.map((c, idx) => (
            <div key={idx} className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700/60 rounded-xl p-4 space-y-2 hover:border-indigo-500 transition-all">
              <div className="flex items-center justify-between text-xs font-bold text-slate-900 dark:text-white">
                <span className="bg-slate-200 dark:bg-slate-800 px-2 py-0.5 rounded text-indigo-600 dark:text-indigo-400">{c.from}</span>
                <ArrowRight className="w-4 h-4 text-slate-400" />
                <span className="bg-indigo-600 text-white px-2 py-0.5 rounded">{c.to}</span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">{c.desc}</p>
              <div className="flex items-center space-x-1 text-[11px] text-emerald-600 dark:text-emerald-400 font-medium">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Fully Supported</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
