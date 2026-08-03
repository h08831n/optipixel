import React from "react";
import { JobHistoryEntry, LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { History, Trash2, CheckCircle } from "lucide-react";
import { formatBytes } from "../utils/formatUtils";

interface HistoryPageProps {
  history: JobHistoryEntry[];
  onClearHistory: () => void;
  lang: LanguageCode;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ history, onClearHistory, lang }) => {
  const t: TranslationSchema = translations[lang] || translations.en;

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-700/60 pb-4">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
              <History className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white">Optimization Job History</h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">Local record of completed batch optimization runs</p>
            </div>
          </div>

          {history.length > 0 && (
            <button
              onClick={onClearHistory}
              className="text-xs text-slate-500 hover:text-red-500 font-semibold flex items-center space-x-1"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear History</span>
            </button>
          )}
        </div>

        {history.length === 0 ? (
          <div className="text-center py-12 text-slate-400 text-xs">
            No optimization jobs recorded yet. Run a batch job on the Optimize page to log history.
          </div>
        ) : (
          <div className="border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
            <table className="w-full text-left rtl:text-right text-xs">
              <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 font-bold border-b border-slate-200 dark:border-slate-700">
                <tr>
                  <th className="p-3">Job ID</th>
                  <th className="p-3">Timestamp</th>
                  <th className="p-3">Operation</th>
                  <th className="p-3">Files Processed</th>
                  <th className="p-3">Space Saved</th>
                  <th className="p-3">Duration</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-200 font-medium">
                {history.map((entry) => (
                  <tr key={entry.id}>
                    <td className="p-3 font-bold">#{entry.id}</td>
                    <td className="p-3 text-slate-500">{entry.timestamp}</td>
                    <td className="p-3">{entry.operation}</td>
                    <td className="p-3 font-bold">{entry.filesProcessed} files</td>
                    <td className="p-3 font-bold text-emerald-600 dark:text-emerald-400">{formatBytes(entry.savedBytes)}</td>
                    <td className="p-3">{entry.durationSeconds}s</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
