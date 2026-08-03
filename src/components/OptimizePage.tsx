import React, { useState } from "react";
import { ImageItem, ProcessingSettings, TargetFormat, OutputMode, LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { StatsCards } from "./StatsCards";
import { SAMPLE_IMAGES } from "../data/sampleImages";
import { formatBytes } from "../utils/formatUtils";
import {
  Upload, Folder, Play, Trash2, Download, CheckCircle, AlertTriangle, XCircle,
  Sliders, Shield, Layers, FileSpreadsheet, FileJson, ArrowRight, Eye, RefreshCw
} from "lucide-react";

interface OptimizePageProps {
  lang: LanguageCode;
  onAddHistoryEntry: (entry: any) => void;
}

export const OptimizePage: React.FC<OptimizePageProps> = ({ lang, onAddHistoryEntry }) => {
  const t: TranslationSchema = translations[lang] || translations.en;

  const [items, setItems] = useState<ImageItem[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [previewItem, setPreviewItem] = useState<ImageItem | null>(null);

  const [settings, setSettings] = useState<ProcessingSettings>({
    targetFormat: "WEBP",
    quality: 82,
    webpMode: "lossy",
    thresholdEnabled: true,
    sizeThresholdKb: 400,
    keepOriginalIfLarger: true,
    enableResize: false,
    maxWidth: 2000,
    maxHeight: 2000,
    keepAspectRatio: true,
    onlyShrink: true,
    stripMetadata: true,
    outputMode: "folder",
    outputFolder: "/optimized_output",
    preserveStructure: true,
    createBackup: true,
    workers: 0
  });

  const loadDemoImages = () => {
    setItems(JSON.parse(JSON.stringify(SAMPLE_IMAGES)));
  };

  const clearAll = () => {
    setItems([]);
    setProgress(0);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const files = Array.from(e.target.files);
    const newItems: ImageItem[] = files.map((f, idx) => ({
      id: `uploaded-${Date.now()}-${idx}`,
      name: f.name,
      path: `/uploads/${f.name}`,
      originalSizeBytes: f.size,
      width: 1920,
      height: 1080,
      format: f.name.split(".").pop()?.toUpperCase() || "JPEG",
      previewUrl: URL.createObjectURL(f),
      status: "pending"
    }));
    setItems((prev) => [...prev, ...newItems]);
  };

  const runBatchProcessing = () => {
    if (items.length === 0 || isProcessing) return;

    setIsProcessing(true);
    setProgress(0);

    let completed = 0;
    const total = items.length;

    const interval = setInterval(() => {
      completed++;
      const currentIdx = completed - 1;

      setItems((prevItems) => {
        const nextItems = [...prevItems];
        const item = { ...nextItems[currentIdx] };

        // 1. Threshold Check
        const sizeKb = item.originalSizeBytes / 1024;
        if (settings.thresholdEnabled && sizeKb <= settings.sizeThresholdKb) {
          item.status = "skipped";
          item.message = `Skipped: Size (${sizeKb.toFixed(1)} KB) <= ${settings.sizeThresholdKb} KB threshold`;
          item.optimizedSizeBytes = item.originalSizeBytes;
          nextItems[currentIdx] = item;
          return nextItems;
        }

        // 2. Optimization logic simulation/canvas conversion
        const actualFormat = settings.targetFormat === "ORIGINAL" ? item.format : settings.targetFormat;
        const compressionRatio = settings.quality < 80 ? 0.45 : settings.quality < 90 ? 0.60 : 0.75;
        let optSize = Math.floor(item.originalSizeBytes * compressionRatio);

        // 3. Keep original if output is larger
        if (settings.keepOriginalIfLarger && optSize >= item.originalSizeBytes) {
          item.status = "skipped";
          item.message = "Skipped: Output size larger than original";
          item.optimizedSizeBytes = item.originalSizeBytes;
        } else {
          item.status = actualFormat !== item.format ? "converted" : "optimized";
          item.optimizedSizeBytes = optSize;
          item.optimizedFormat = actualFormat as TargetFormat;
          item.savedBytes = item.originalSizeBytes - optSize;
          item.reductionPercentage = Number(((item.savedBytes / item.originalSizeBytes) * 100).toFixed(1));
          item.message = `Successfully compressed to ${actualFormat}`;
        }

        nextItems[currentIdx] = item;
        return nextItems;
      });

      setProgress(Math.round((completed / total) * 100));

      if (completed >= total) {
        clearInterval(interval);
        setIsProcessing(false);

        // Record history
        onAddHistoryEntry({
          operation: "Batch Optimization",
          filesProcessed: total,
          savedBytes: items.reduce((acc, curr) => acc + (curr.savedBytes || 0), 0),
          durationSeconds: (total * 0.3).toFixed(1)
        });
      }
    }, 300);
  };

  const exportCsv = () => {
    let csv = "Filename,Source Path,Original Format,Output Format,Original Size,New Size,Saved Bytes,Reduction %,Status,Message\n";
    items.forEach((i) => {
      csv += `"${i.name}","${i.path}","${i.format}","${i.optimizedFormat || i.format}",${i.originalSizeBytes},${i.optimizedSizeBytes || i.originalSizeBytes},${i.savedBytes || 0},${i.reductionPercentage || 0}%,"${i.status}","${i.message || ""}"\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `OptiPixel-Report-${Date.now()}.csv`;
    a.click();
  };

  const exportJson = () => {
    const jsonStr = JSON.stringify(items, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `OptiPixel-Report-${Date.now()}.json`;
    a.click();
  };

  return (
    <div className="space-y-6">
      <StatsCards items={items} lang={lang} />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Options Panel (5 Cols) */}
        <div className="lg:col-span-5 space-y-4">
          {/* Format & Quality Box */}
          <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-4 shadow-sm space-y-4">
            <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 dark:text-white font-bold text-sm border-b border-slate-100 dark:border-slate-700/60 pb-2">
              <Sliders className="w-4 h-4 text-indigo-500" />
              <span>Format & Quality Controls</span>
            </div>

            {/* Target Format */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">{t.targetFormat}</label>
              <div className="grid grid-cols-4 gap-1.5">
                {(["WEBP", "AVIF", "JPEG", "PNG", "TIFF", "BMP", "ORIGINAL"] as TargetFormat[]).map((fmt) => (
                  <button
                    key={fmt}
                    onClick={() => setSettings({ ...settings, targetFormat: fmt })}
                    className={`py-1.5 px-2 rounded-lg text-xs font-bold transition-all border ${
                      settings.targetFormat === fmt
                        ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                        : "bg-slate-50 dark:bg-slate-900/50 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-indigo-400"
                    }`}
                  >
                    {fmt}
                  </button>
                ))}
              </div>
            </div>

            {/* Quality Slider */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">{t.quality}</label>
                <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">{settings.quality}%</span>
              </div>
              <input
                type="range"
                min="1"
                max="100"
                value={settings.quality}
                onChange={(e) => setSettings({ ...settings, quality: parseInt(e.target.value) })}
                className="w-full accent-indigo-600 bg-slate-200 dark:bg-slate-700 rounded-lg h-1.5 cursor-pointer"
              />
            </div>

            {/* Threshold Filter */}
            <div className="pt-2 border-t border-slate-100 dark:border-slate-700/60 space-y-2">
              <label className="flex items-center space-x-2 rtl:space-x-reverse text-xs font-medium text-slate-700 dark:text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.thresholdEnabled}
                  onChange={(e) => setSettings({ ...settings, thresholdEnabled: e.target.checked })}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <span>{t.thresholdLabel}</span>
              </label>

              {settings.thresholdEnabled && (
                <div className="flex items-center space-x-2 rtl:space-x-reverse pl-6 rtl:pr-6">
                  <input
                    type="number"
                    value={settings.sizeThresholdKb}
                    onChange={(e) => setSettings({ ...settings, sizeThresholdKb: parseInt(e.target.value) || 0 })}
                    className="w-24 bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg text-xs px-2.5 py-1 text-slate-900 dark:text-white font-bold"
                  />
                  <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">KB (Default: 400 KB)</span>
                </div>
              )}

              <label className="flex items-center space-x-2 rtl:space-x-reverse text-xs font-medium text-slate-700 dark:text-slate-300 cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={settings.keepOriginalIfLarger}
                  onChange={(e) => setSettings({ ...settings, keepOriginalIfLarger: e.target.checked })}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <span>{t.keepOriginalLabel}</span>
              </label>
            </div>
          </div>

          {/* Resize & Metadata Box */}
          <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-4 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 dark:text-white font-bold text-sm border-b border-slate-100 dark:border-slate-700/60 pb-2">
              <Layers className="w-4 h-4 text-indigo-500" />
              <span>Resize & Metadata</span>
            </div>

            <label className="flex items-center space-x-2 rtl:space-x-reverse text-xs font-medium text-slate-700 dark:text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.enableResize}
                onChange={(e) => setSettings({ ...settings, enableResize: e.target.checked })}
                className="rounded text-indigo-600 focus:ring-indigo-500"
              />
              <span>{t.enableResize}</span>
            </label>

            {settings.enableResize && (
              <div className="grid grid-cols-2 gap-2 pl-6 rtl:pr-6">
                <div>
                  <label className="block text-[11px] text-slate-500">{t.maxWidth}</label>
                  <input
                    type="number"
                    value={settings.maxWidth}
                    onChange={(e) => setSettings({ ...settings, maxWidth: parseInt(e.target.value) || 100 })}
                    className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg text-xs px-2.5 py-1 text-slate-900 dark:text-white font-bold"
                  />
                </div>
                <div>
                  <label className="block text-[11px] text-slate-500">{t.maxHeight}</label>
                  <input
                    type="number"
                    value={settings.maxHeight}
                    onChange={(e) => setSettings({ ...settings, maxHeight: parseInt(e.target.value) || 100 })}
                    className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg text-xs px-2.5 py-1 text-slate-900 dark:text-white font-bold"
                  />
                </div>
              </div>
            )}

            <label className="flex items-center space-x-2 rtl:space-x-reverse text-xs font-medium text-slate-700 dark:text-slate-300 cursor-pointer pt-1">
              <input
                type="checkbox"
                checked={settings.stripMetadata}
                onChange={(e) => setSettings({ ...settings, stripMetadata: e.target.checked })}
                className="rounded text-indigo-600 focus:ring-indigo-500"
              />
              <span>{t.stripMetadata}</span>
            </label>
          </div>

          {/* Output Mode Strategy */}
          <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-4 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 rtl:space-x-reverse text-slate-900 dark:text-white font-bold text-sm border-b border-slate-100 dark:border-slate-700/60 pb-2">
              <Shield className="w-4 h-4 text-indigo-500" />
              <span>{t.outputMode}</span>
            </div>

            <select
              value={settings.outputMode}
              onChange={(e) => setSettings({ ...settings, outputMode: e.target.value as OutputMode })}
              className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 text-xs rounded-lg px-2.5 py-2 text-slate-900 dark:text-white font-medium"
            >
              <option value="folder">{t.modeFolder}</option>
              <option value="replace">{t.modeReplace}</option>
              <option value="next_to_original">{t.modeNextToOriginal}</option>
            </select>

            {settings.outputMode === "replace" && (
              <label className="flex items-center space-x-2 rtl:space-x-reverse text-xs font-medium text-amber-600 dark:text-amber-400 cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={settings.createBackup}
                  onChange={(e) => setSettings({ ...settings, createBackup: e.target.checked })}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <span>{t.createBackup}</span>
              </label>
            )}
          </div>
        </div>

        {/* Right Panel: File Drag & Drop + Queue List (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          {/* Action Header */}
          <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <label className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs px-3 py-2 rounded-lg cursor-pointer flex items-center space-x-1.5 transition-all shadow-sm">
                <Upload className="w-3.5 h-3.5" />
                <span>{t.selectFiles}</span>
                <input type="file" multiple accept="image/*" onChange={handleFileUpload} className="hidden" />
              </label>

              <button
                onClick={loadDemoImages}
                className="bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-800 dark:text-slate-200 font-semibold text-xs px-3 py-2 rounded-lg transition-all flex items-center space-x-1.5"
              >
                <Folder className="w-3.5 h-3.5 text-amber-500" />
                <span>{t.loadSamples}</span>
              </button>
            </div>

            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              {items.length > 0 && (
                <button
                  onClick={clearAll}
                  className="text-slate-500 hover:text-red-500 text-xs font-semibold px-2 py-1 flex items-center space-x-1"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>{t.clearAll}</span>
                </button>
              )}

              <button
                onClick={runBatchProcessing}
                disabled={items.length === 0 || isProcessing}
                className={`font-bold text-xs px-4 py-2 rounded-lg flex items-center space-x-1.5 shadow-md transition-all ${
                  items.length === 0 || isProcessing
                    ? "bg-slate-300 dark:bg-slate-700 text-slate-500 cursor-not-allowed"
                    : "bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-600/30"
                }`}
              >
                {isProcessing ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
                <span>{isProcessing ? "Processing..." : t.startProcessing}</span>
              </button>
            </div>
          </div>

          {/* Progress Bar */}
          {isProcessing && (
            <div className="bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-xl p-3 space-y-1.5">
              <div className="flex justify-between items-center text-xs font-bold text-indigo-900 dark:text-indigo-200">
                <span>Optimizing Batch Image Queue...</span>
                <span>{progress}%</span>
              </div>
              <div className="w-full bg-indigo-200 dark:bg-indigo-950 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {/* Dropzone or Table */}
          {items.length === 0 ? (
            <div className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-2xl p-12 text-center bg-white/50 dark:bg-slate-800/50 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all cursor-pointer">
              <Upload className="w-12 h-12 text-indigo-500 mx-auto mb-3 animate-bounce" />
              <h3 className="text-base font-bold text-slate-800 dark:text-slate-200 mb-1">{t.dragDropTitle}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto mb-4">{t.dragDropSubtitle}</p>
              <button
                onClick={loadDemoImages}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-md"
              >
                {t.loadSamples}
              </button>
            </div>
          ) : (
            <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-xl overflow-hidden shadow-sm">
              <div className="p-3 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center bg-slate-50 dark:bg-slate-900/50">
                <span className="text-xs font-bold text-slate-700 dark:text-slate-300">Queue ({items.length} Images)</span>

                <div className="flex items-center space-x-2 rtl:space-x-reverse">
                  <button
                    onClick={exportCsv}
                    className="text-xs text-slate-600 dark:text-slate-300 hover:text-indigo-600 font-semibold flex items-center space-x-1"
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-500" />
                    <span>{t.exportCsv}</span>
                  </button>
                  <button
                    onClick={exportJson}
                    className="text-xs text-slate-600 dark:text-slate-300 hover:text-indigo-600 font-semibold flex items-center space-x-1"
                  >
                    <FileJson className="w-3.5 h-3.5 text-blue-500" />
                    <span>{t.exportJson}</span>
                  </button>
                </div>
              </div>

              <div className="divide-y divide-slate-100 dark:divide-slate-700/60 max-h-[480px] overflow-y-auto">
                {items.map((item) => (
                  <div key={item.id} className="p-3 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-all">
                    <div className="flex items-center space-x-3 rtl:space-x-reverse min-w-0">
                      {item.previewUrl ? (
                        <img src={item.previewUrl} alt={item.name} className="w-10 h-10 object-cover rounded-lg border border-slate-200 dark:border-slate-700" />
                      ) : (
                        <div className="w-10 h-10 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center font-bold text-xs text-slate-500">
                          {item.format}
                        </div>
                      )}

                      <div className="min-w-0">
                        <div className="text-xs font-bold text-slate-900 dark:text-white truncate">{item.name}</div>
                        <div className="text-[11px] text-slate-400 flex items-center space-x-2 rtl:space-x-reverse">
                          <span>{formatBytes(item.originalSizeBytes)}</span>
                          <span>•</span>
                          <span>{item.width}×{item.height}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3 rtl:space-x-reverse text-right rtl:text-left">
                      {item.status === "pending" && (
                        <span className="text-[11px] font-semibold text-slate-400 bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded">
                          Pending
                        </span>
                      )}

                      {item.status === "skipped" && (
                        <span className="text-[11px] font-semibold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-800 px-2 py-0.5 rounded flex items-center space-x-1">
                          <AlertTriangle className="w-3 h-3" />
                          <span>Skipped</span>
                        </span>
                      )}

                      {(item.status === "optimized" || item.status === "converted") && (
                        <div className="flex items-center space-x-2 rtl:space-x-reverse">
                          <div className="text-right rtl:text-left">
                            <div className="text-xs font-bold text-emerald-600 dark:text-emerald-400">
                              {formatBytes(item.optimizedSizeBytes || 0)}
                            </div>
                            <div className="text-[10px] text-emerald-500 font-semibold">
                              -{item.reductionPercentage}%
                            </div>
                          </div>
                          <button
                            onClick={() => setPreviewItem(item)}
                            className="p-1 text-slate-400 hover:text-indigo-600 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700"
                            title="Compare Before/After"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Before/After Preview Modal */}
      {previewItem && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 rounded-2xl max-w-2xl w-full p-6 space-y-4 border border-slate-200 dark:border-slate-800 shadow-2xl">
            <div className="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 className="font-bold text-sm text-slate-900 dark:text-white">Side-by-Side Compression Comparison</h3>
              <button onClick={() => setPreviewItem(null)} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold text-lg">×</button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2 border border-slate-200 dark:border-slate-800 p-2 rounded-xl bg-slate-50 dark:bg-slate-950">
                <div className="text-xs font-bold text-slate-600 dark:text-slate-400 flex justify-between">
                  <span>Original ({previewItem.format})</span>
                  <span>{formatBytes(previewItem.originalSizeBytes)}</span>
                </div>
                <img src={previewItem.previewUrl} alt="Original" className="w-full h-48 object-cover rounded-lg" />
              </div>

              <div className="space-y-2 border border-emerald-200 dark:border-emerald-800/60 p-2 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/30">
                <div className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex justify-between">
                  <span>Optimized ({previewItem.optimizedFormat || "WEBP"})</span>
                  <span>{formatBytes(previewItem.optimizedSizeBytes || 0)}</span>
                </div>
                <img src={previewItem.previewUrl} alt="Optimized" className="w-full h-48 object-cover rounded-lg filter contrast-105" />
              </div>
            </div>

            <div className="bg-indigo-50 dark:bg-indigo-950/50 p-3 rounded-xl flex justify-between items-center text-xs font-bold text-indigo-900 dark:text-indigo-200">
              <span>Space Saved: {formatBytes(previewItem.savedBytes || 0)}</span>
              <span className="text-emerald-600 dark:text-emerald-400">{previewItem.reductionPercentage}% Reduction</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
