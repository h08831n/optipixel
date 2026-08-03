import React, { useState } from "react";
import { LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { Search, AlertTriangle, AlertOctagon, CheckCircle2, FileSearch, ArrowRight } from "lucide-react";
import { SAMPLE_IMAGES } from "../data/sampleImages";
import { formatBytes } from "../utils/formatUtils";

interface AuditPageProps {
  lang: LanguageCode;
}

export const AuditPage: React.FC<AuditPageProps> = ({ lang }) => {
  const t: TranslationSchema = translations[lang] || translations.en;
  const [scanned, setScanned] = useState(false);

  const totalFiles = SAMPLE_IMAGES.length;
  const totalVolume = SAMPLE_IMAGES.reduce((acc, curr) => acc + curr.originalSizeBytes, 0);
  const over400Kb = SAMPLE_IMAGES.filter((i) => i.originalSizeBytes > 400 * 1024).length;
  const over1Mb = SAMPLE_IMAGES.filter((i) => i.originalSizeBytes > 1024 * 1024).length;

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-700/60 pb-4">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-900/40 flex items-center justify-center text-amber-600 dark:text-amber-400">
              <Search className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white">SEO & Web Performance Image Audit (Read-Only)</h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">Analyze media folders without modifying files. Identifies oversized images harming Core Web Vitals.</p>
            </div>
          </div>

          <button
            onClick={() => setScanned(true)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-md flex items-center space-x-1.5"
          >
            <FileSearch className="w-4 h-4" />
            <span>Scan Folder for Audit</span>
          </button>
        </div>

        {/* Audit Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-slate-50 dark:bg-slate-900/50 p-3 rounded-xl border border-slate-200 dark:border-slate-700">
            <span className="text-xs font-semibold text-slate-500">Scanned Images</span>
            <div className="text-xl font-bold text-slate-900 dark:text-white mt-1">{scanned ? totalFiles : 0}</div>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900/50 p-3 rounded-xl border border-slate-200 dark:border-slate-700">
            <span className="text-xs font-semibold text-slate-500">Total Size</span>
            <div className="text-xl font-bold text-slate-900 dark:text-white mt-1">{scanned ? formatBytes(totalVolume) : "0 B"}</div>
          </div>

          <div className="bg-amber-50 dark:bg-amber-950/40 p-3 rounded-xl border border-amber-200 dark:border-amber-800">
            <span className="text-xs font-semibold text-amber-600 dark:text-amber-400">Over 400 KB</span>
            <div className="text-xl font-bold text-amber-700 dark:text-amber-300 mt-1">{scanned ? over400Kb : 0}</div>
          </div>

          <div className="bg-red-50 dark:bg-red-950/40 p-3 rounded-xl border border-red-200 dark:border-red-800">
            <span className="text-xs font-semibold text-red-600 dark:text-red-400">Over 1 MB (Critical)</span>
            <div className="text-xl font-bold text-red-700 dark:text-red-300 mt-1">{scanned ? over1Mb : 0}</div>
          </div>
        </div>

        {/* Results Table */}
        {scanned ? (
          <div className="border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
            <table className="w-full text-left rtl:text-right text-xs">
              <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 font-bold border-b border-slate-200 dark:border-slate-700">
                <tr>
                  <th className="p-3">Filename</th>
                  <th className="p-3">Format</th>
                  <th className="p-3">Dimensions</th>
                  <th className="p-3">Size</th>
                  <th className="p-3">Audit Recommendation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-200 font-medium">
                {SAMPLE_IMAGES.map((img) => {
                  const sizeMb = img.originalSizeBytes / (1024 * 1024);
                  let rec = { text: "Optimal - No action needed", color: "text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30", icon: CheckCircle2 };
                  if (sizeMb > 1.0) {
                    rec = { text: "CRITICAL: Convert to WebP & Resize to max 2000px", color: "text-red-600 bg-red-50 dark:bg-red-900/30", icon: AlertOctagon };
                  } else if (img.originalSizeBytes > 400 * 1024) {
                    rec = { text: "WARNING: Convert to WebP / Lossy Compress", color: "text-amber-600 bg-amber-50 dark:bg-amber-900/30", icon: AlertTriangle };
                  }
                  const Icon = rec.icon;

                  return (
                    <tr key={img.id}>
                      <td className="p-3 font-bold truncate max-w-[200px]">{img.name}</td>
                      <td className="p-3">{img.format}</td>
                      <td className="p-3">{img.width}×{img.height}</td>
                      <td className="p-3 font-bold">{formatBytes(img.originalSizeBytes)}</td>
                      <td className="p-3">
                        <span className={`inline-flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-1 rounded-lg font-bold text-[11px] ${rec.color}`}>
                          <Icon className="w-3.5 h-3.5" />
                          <span>{rec.text}</span>
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12 text-slate-400 text-xs">
            Click "Scan Folder for Audit" to analyze web image performance without making changes.
          </div>
        )}
      </div>
    </div>
  );
};
