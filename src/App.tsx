import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { OptimizePage } from "./components/OptimizePage";
import { ConvertPage } from "./components/ConvertPage";
import { AuditPage } from "./components/AuditPage";
import { HistoryPage } from "./components/HistoryPage";
import { SettingsPage } from "./components/SettingsPage";
import { AboutPage } from "./components/AboutPage";
import { UpdaterModal } from "./components/UpdaterModal";
import { JobHistoryEntry, LanguageCode } from "./types";
import { isRtlLanguage } from "./i18n";

export default function App() {
  const [activeTab, setActiveTab] = useState("optimize");
  const [lang, setLang] = useState<LanguageCode>("fa");
  const [darkMode, setDarkMode] = useState(true);
  const [history, setHistory] = useState<JobHistoryEntry[]>([]);
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [releaseInfo, setReleaseInfo] = useState<any>(null);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  useEffect(() => {
    fetch("https://api.github.com/repos/h08831n/OptiPixel/releases/latest")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.tag_name) {
          setReleaseInfo(data);
        }
      })
      .catch(() => {});
  }, []);

  const isRtl = isRtlLanguage(lang);

  const addHistoryEntry = (entry: Omit<JobHistoryEntry, "id" | "timestamp">) => {
    const newEntry: JobHistoryEntry = {
      id: history.length + 1,
      timestamp: new Date().toLocaleString(),
      ...entry
    };
    setHistory((prev) => [newEntry, ...prev]);
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className={`min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans ${darkMode ? "dark" : ""}`} dir={isRtl ? "rtl" : "ltr"}>
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        lang={lang}
        setLang={setLang}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        onOpenUpdateModal={() => setIsUpdateModalOpen(true)}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === "optimize" && (
          <OptimizePage lang={lang} onAddHistoryEntry={addHistoryEntry} />
        )}
        {activeTab === "convert" && <ConvertPage lang={lang} />}
        {activeTab === "audit" && <AuditPage lang={lang} />}
        {activeTab === "history" && (
          <HistoryPage history={history} onClearHistory={clearHistory} lang={lang} />
        )}
        {activeTab === "settings" && <SettingsPage lang={lang} />}
        {activeTab === "about" && (
          <AboutPage lang={lang} onOpenUpdateModal={() => setIsUpdateModalOpen(true)} />
        )}
      </main>

      <UpdaterModal
        isOpen={isUpdateModalOpen}
        onClose={() => setIsUpdateModalOpen(false)}
        releaseInfo={releaseInfo}
        lang={lang}
      />
    </div>
  );
}
