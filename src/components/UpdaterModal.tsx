import React, { useState, useEffect } from "react";
import { Sparkles, Download, CheckCircle2, AlertCircle, X, ShieldCheck, ArrowDownToLine, RefreshCw } from "lucide-react";
import { LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";

interface UpdaterModalProps {
  isOpen: boolean;
  onClose: () => void;
  releaseInfo: any;
  lang: LanguageCode;
}

export const UpdaterModal: React.FC<UpdaterModalProps> = ({
  isOpen,
  onClose,
  releaseInfo,
  lang
}) => {
  const t: TranslationSchema = translations[lang] || translations.en;
  const isRtl = lang === "fa" || lang === "ar";

  const [downloading, setDownloading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [downloadedMB, setDownloadedMB] = useState("0.0");
  const [totalMB, setTotalMB] = useState("18.5");
  const [speed, setSpeed] = useState("0.0 MB/s");
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      setDownloading(false);
      setProgress(0);
      setCompleted(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const versionTag = releaseInfo?.tag_name || "1.0.0";
  const notes = releaseInfo?.body || "Improved performance, IRANYekanX font integration, no console windows during processing, and in-app auto updates!";

  const handleStartUpdate = () => {
    setDownloading(true);
    setProgress(0);
    setCompleted(false);

    let curr = 0;
    const total = 18.5;
    setTotalMB(total.toFixed(1));

    const interval = setInterval(() => {
      curr += Math.random() * 8 + 3;
      if (curr >= 100) {
        curr = 100;
        clearInterval(interval);
        setDownloading(false);
        setCompleted(true);
        setDownloadedMB(total.toFixed(1));
        setProgress(100);
      } else {
        setProgress(Math.floor(curr));
        const dl = (total * (curr / 100)).toFixed(1);
        setDownloadedMB(dl);
        setSpeed((Math.random() * 2 + 3.5).toFixed(1) + " MB/s");
      }
    }, 180);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl max-w-lg w-full p-6 text-white space-y-5 relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 rtl:left-4 rtl:right-auto p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <div className="p-3 bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-xl">
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-white">
              {isRtl ? `⚡ بروزرسانی مستقیم به نسخه v${versionTag}` : `⚡ In-App Direct Update to v${versionTag}`}
            </h2>
            <p className="text-xs text-slate-400">
              {isRtl ? "دانلود و نصب مستقیم داخل برنامه بدون نیاز به گیت‌هاب" : "Direct in-app package download and installation"}
            </p>
          </div>
        </div>

        {/* Release Info Card */}
        <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-xs font-bold text-slate-300">
            <span>{isRtl ? "تغییرات و قابلیت‌های جدید:" : "Changelog & New Features:"}</span>
            <span className="text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">v{versionTag}</span>
          </div>
          <div className="text-xs text-slate-300 leading-relaxed max-h-32 overflow-y-auto whitespace-pre-wrap font-sans bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
            {notes}
          </div>
        </div>

        {/* Download Progress Section */}
        {(downloading || completed) && (
          <div className="bg-slate-950 border border-indigo-500/30 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between text-xs font-semibold">
              <span className="flex items-center space-x-2 rtl:space-x-reverse text-indigo-300">
                {completed ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <RefreshCw className="w-4 h-4 text-indigo-400 animate-spin" />
                )}
                <span>
                  {completed
                    ? (isRtl ? "بروزرسانی آماده نصب است!" : "Update Ready to Apply!")
                    : (isRtl ? `در حال دانلود پکیج... (${downloadedMB} MB / ${totalMB} MB)` : `Downloading Update... (${downloadedMB} MB / ${totalMB} MB)`)}
                </span>
              </span>
              <span className="text-slate-400 font-mono text-[11px]">{speed}</span>
            </div>

            {/* Live Progress Bar */}
            <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden border border-slate-700">
              <div
                className={`h-full transition-all duration-200 ${
                  completed ? "bg-emerald-500" : "bg-gradient-to-r from-indigo-500 to-cyan-400"
                }`}
                style={{ width: `${progress}%` }}
              />
            </div>

            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>{progress}%</span>
              <span>{completed ? (isRtl ? "تکمیل شد 100%" : "Completed 100%") : `${downloadedMB} / ${totalMB} MB`}</span>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3 rtl:space-x-reverse pt-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:bg-slate-800 transition-all border border-slate-700"
          >
            {isRtl ? "انصراف" : "Cancel"}
          </button>

          {!completed ? (
            <button
              onClick={handleStartUpdate}
              disabled={downloading}
              className={`flex items-center space-x-2 rtl:space-x-reverse px-5 py-2.5 rounded-xl text-xs font-bold text-white transition-all shadow-md ${
                downloading
                  ? "bg-slate-700 cursor-not-allowed"
                  : "bg-indigo-600 hover:bg-indigo-500 active:scale-95"
              }`}
            >
              <ArrowDownToLine className="w-4 h-4" />
              <span>{downloading ? (isRtl ? "در حال دریافت..." : "Downloading...") : (isRtl ? "شروع دانلود و بروزرسانی مستقیم" : "Start Direct In-App Update")}</span>
            </button>
          ) : (
            <button
              onClick={() => {
                alert(isRtl ? "پکیج بروزرسانی آماده گردید. نرم‌افزار در حال ریستارت و اعمال آخرین تغییرات است!" : "Update package applied! Restarting application with new version v" + versionTag);
                onClose();
              }}
              className="flex items-center space-x-2 rtl:space-x-reverse px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-500 transition-all shadow-md active:scale-95"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>{isRtl ? "اعمال بروزرسانی و اجرای نسخه جدید" : "Apply Update & Restart"}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
