import React from "react";
import { ImageItem } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { LanguageCode } from "../types";
import { formatBytes } from "../utils/formatUtils";
import { Images, HardDrive, ShieldCheck, TrendingDown } from "lucide-react";

interface StatsCardsProps {
  items: ImageItem[];
  lang: LanguageCode;
}

export const StatsCards: React.FC<StatsCardsProps> = ({ items, lang }) => {
  const t: TranslationSchema = translations[lang] || translations.en;

  const totalCount = items.length;
  const originalTotalBytes = items.reduce((acc, curr) => acc + curr.originalSizeBytes, 0);

  const processedItems = items.filter((i) => i.status === "optimized" || i.status === "converted");
  const optimizedTotalBytes = items.reduce((acc, curr) => {
    if (curr.status === "optimized" || curr.status === "converted") {
      return acc + (curr.optimizedSizeBytes || curr.originalSizeBytes);
    }
    return acc + curr.originalSizeBytes;
  }, 0);

  const savedBytes = Math.max(0, originalTotalBytes - optimizedTotalBytes);
  const reductionPct = originalTotalBytes > 0 ? ((savedBytes / originalTotalBytes) * 100).toFixed(1) : "0.0";

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
      {/* Card 1 */}
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-3.5 shadow-sm">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">{t.totalImages}</span>
          <div className="w-7 h-7 rounded-lg bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
            <Images className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl font-bold text-slate-900 dark:text-white">{totalCount}</div>
        <div className="text-[11px] text-slate-400 mt-0.5">{processedItems.length} {t.processed}</div>
      </div>

      {/* Card 2 */}
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-3.5 shadow-sm">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">{t.originalSize}</span>
          <div className="w-7 h-7 rounded-lg bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center text-amber-600 dark:text-amber-400">
            <HardDrive className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl font-bold text-slate-900 dark:text-white">{formatBytes(originalTotalBytes)}</div>
        <div className="text-[11px] text-slate-400 mt-0.5">Uncompressed baseline</div>
      </div>

      {/* Card 3 */}
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-3.5 shadow-sm">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">{t.finalSize}</span>
          <div className="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl font-bold text-slate-900 dark:text-white">{formatBytes(optimizedTotalBytes)}</div>
        <div className="text-[11px] text-emerald-600 dark:text-emerald-400 font-medium mt-0.5">-{reductionPct}% reduced</div>
      </div>

      {/* Card 4 */}
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-3.5 shadow-sm">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">{t.spaceSaved}</span>
          <div className="w-7 h-7 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
            <TrendingDown className="w-4 h-4" />
          </div>
        </div>
        <div className="text-xl font-bold text-indigo-600 dark:text-indigo-400">{formatBytes(savedBytes)}</div>
        <div className="text-[11px] text-slate-400 mt-0.5">Bandwidth saved</div>
      </div>
    </div>
  );
};
