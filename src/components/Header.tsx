import React from "react";
import { Zap, RefreshCw, Search, History, Settings, Info, Globe, Moon, Sun, Heart } from "lucide-react";
import { LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { Logo } from "./Logo";

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  lang: LanguageCode;
  setLang: (lang: LanguageCode) => void;
  darkMode: boolean;
  setDarkMode: (val: boolean) => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  lang,
  setLang,
  darkMode,
  setDarkMode
}) => {
  const t: TranslationSchema = translations[lang] || translations.en;

  const navItems = [
    { id: "optimize", label: t.optimize, icon: Zap },
    { id: "convert", label: t.convert, icon: RefreshCw },
    { id: "audit", label: t.audit, icon: Search },
    { id: "history", label: t.history, icon: History },
    { id: "settings", label: t.settings, icon: Settings },
    { id: "about", label: t.about, icon: Info }
  ];

  return (
    <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-40 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <div className="flex items-center space-x-3 rtl:space-x-reverse cursor-pointer" onClick={() => setActiveTab("optimize")}>
            <Logo size={36} className="w-9 h-9 drop-shadow" />
            <div>
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <span className="font-extrabold text-lg tracking-tight text-white">{t.appName}</span>
                <span className="text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-1.5 py-0.5 rounded">v0.1.0</span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">{t.tagline}</p>
            </div>
          </div>

          {/* Nav Tabs */}
          <nav className="hidden md:flex items-center space-x-1 rtl:space-x-reverse">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-1.5 rtl:space-x-reverse px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? "bg-indigo-600 text-white shadow-sm"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Controls */}
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            {/* Donate Quick Link */}
            <button
              onClick={() => setActiveTab("about")}
              className="hidden lg:flex items-center space-x-1 rtl:space-x-reverse bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/30 px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all"
              title={t.donate}
            >
              <Heart className="w-3.5 h-3.5 fill-current text-amber-400" />
              <span>{t.donate}</span>
            </button>

            {/* Language Selector */}
            <div className="relative flex items-center">
              <Globe className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 rtl:right-2.5 pointer-events-none" />
              <select
                value={lang}
                onChange={(e) => setLang(e.target.value as LanguageCode)}
                className="bg-slate-800 text-slate-200 border border-slate-700 text-xs rounded-lg pl-8 rtl:pl-2 rtl:pr-8 pr-2 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500 font-medium"
              >
                <option value="en">English</option>
                <option value="fa">فارسی (Persian)</option>
                <option value="de">Deutsch</option>
                <option value="tr">Türkçe</option>
                <option value="ar">العربية</option>
                <option value="fr">Français</option>
                <option value="es">Español</option>
                <option value="ru">Русский</option>
              </select>
            </div>

            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700"
              title="Toggle Theme"
            >
              {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-300" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Nav Bar */}
      <div className="md:hidden flex overflow-x-auto px-2 py-1.5 bg-slate-950 border-t border-slate-800 space-x-1 rtl:space-x-reverse">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center space-x-1 rtl:space-x-reverse px-2.5 py-1.5 rounded-md text-xs font-medium whitespace-nowrap ${
                isActive ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
};
