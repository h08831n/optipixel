import React from "react";
import { LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { Info, ExternalLink, ShieldCheck, Heart } from "lucide-react";

interface AboutPageProps {
  lang: LanguageCode;
}

export const AboutPage: React.FC<AboutPageProps> = ({ lang }) => {
  const t: TranslationSchema = translations[lang] || translations.en;

  return (
    <div className="max-w-3xl mx-auto space-y-6 text-center py-8">
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-8 shadow-sm space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-indigo-600 text-white font-extrabold text-3xl flex items-center justify-center mx-auto shadow-xl shadow-indigo-600/30">
          O
        </div>

        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">{t.appName}</h1>
        <p className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">{t.tagline}</p>

        <p className="text-xs text-slate-600 dark:text-slate-300 max-w-lg mx-auto leading-relaxed">
          OptiPixel is a production-ready Windows desktop application and web solution engineered for web image optimization, batch compression, format conversion, and Core Web Vitals performance tuning.
        </p>

        <div className="pt-4 border-t border-slate-100 dark:border-slate-700/60 flex flex-wrap justify-center gap-6 text-xs text-slate-500 dark:text-slate-400">
          <div><strong className="text-slate-800 dark:text-white">Version:</strong> 0.1.0</div>
          <div><strong className="text-slate-800 dark:text-white">Publisher:</strong> Ahaninja</div>
          <div><strong className="text-slate-800 dark:text-white">GUI Engine:</strong> PySide6 / React</div>
          <div><strong className="text-slate-800 dark:text-white">CLI Core:</strong> ImageMagick 7.x</div>
        </div>

        <div className="pt-4 flex justify-center">
          <a
            href="https://ahaninja.com"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs px-5 py-2.5 rounded-xl transition-all shadow-md"
          >
            <span>Visit Ahaninja Official Site</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
};
