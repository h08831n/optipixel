import React, { useState, useEffect } from "react";
import { LanguageCode } from "../types";
import { TranslationSchema, translations } from "../i18n";
import { ExternalLink, Heart, Bug, Tag, Copy, Check, Github, Sparkles, HelpCircle } from "lucide-react";

interface AboutPageProps {
  lang: LanguageCode;
}

export const AboutPage: React.FC<AboutPageProps> = ({ lang }) => {
  const t: TranslationSchema = translations[lang] || translations.en;
  const [copied, setCopied] = useState(false);
  const [latestRelease, setLatestRelease] = useState<any>(null);
  const [loadingRelease, setLoadingRelease] = useState(false);

  const WALLET_ADDRESS = "UQBHs-6YLo4igSTy470tsyH7g5myvCTAxz6C4e7GothWY9J3";
  const GITHUB_USER = "h08831n";
  const REPO_NAME = "OptiPixel";
  const REPO_URL = `https://github.com/${GITHUB_USER}/${REPO_NAME}`;

  useEffect(() => {
    setLoadingRelease(true);
    fetch(`https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}/releases/latest`)
      .then((res) => res.json())
      .then((data) => {
        if (data && data.tag_name) {
          setLatestRelease(data);
        }
      })
      .catch(() => {})
      .finally(() => setLoadingRelease(false));
  }, []);

  const handleCopyWallet = () => {
    navigator.clipboard.writeText(WALLET_ADDRESS);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-6">
      {/* App Header Card */}
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-8 shadow-sm text-center space-y-4">
        <div className="w-20 h-20 rounded-2xl bg-indigo-600 text-white font-black text-4xl flex items-center justify-center mx-auto shadow-xl shadow-indigo-600/30">
          O
        </div>

        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">{t.appName}</h1>
        <p className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">{t.tagline}</p>

        <p className="text-xs text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
          OptiPixel is an open-source high-performance desktop application and web tool for batch image optimization, format conversion, and media performance auditing. Built with Python (PySide6) and ImageMagick 7.
        </p>

        <div className="pt-4 border-t border-slate-100 dark:border-slate-700/60 flex flex-wrap justify-center gap-6 text-xs text-slate-600 dark:text-slate-400">
          <div><strong className="text-slate-800 dark:text-white">Version:</strong> 0.1.0</div>
          <div><strong className="text-slate-800 dark:text-white">GitHub User:</strong> {GITHUB_USER}</div>
          <div><strong className="text-slate-800 dark:text-white">Repository:</strong> {GITHUB_USER}/{REPO_NAME}</div>
          <div><strong className="text-slate-800 dark:text-white">Engine:</strong> ImageMagick 7 + Python 3.12</div>
        </div>

        <div className="pt-2 flex flex-wrap justify-center gap-3">
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 rtl:space-x-reverse bg-slate-900 hover:bg-black dark:bg-slate-700 dark:hover:bg-slate-600 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all shadow"
          >
            <Github className="w-4 h-4" />
            <span>GitHub Source Code ({GITHUB_USER})</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>

          <a
            href={`${REPO_URL}/issues/new`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 rtl:space-x-reverse bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all shadow"
          >
            <Bug className="w-4 h-4" />
            <span>{t.reportBug}</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* Donation Section */}
      <div className="bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-transparent bg-white dark:bg-slate-800 border border-amber-200 dark:border-amber-500/30 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center space-x-3 rtl:space-x-reverse text-amber-600 dark:text-amber-400">
          <div className="p-2.5 bg-amber-500/20 rounded-xl">
            <Heart className="w-6 h-6 fill-current" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">{t.donate} (Crypto Support)</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Support open-source development via TON / USDT Crypto Wallet</p>
          </div>
        </div>

        <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          If OptiPixel has saved you time or improved your website speed, you can support ongoing development and server costs by sending TON or USDT on the TON network to the crypto address below:
        </p>

        <div className="bg-slate-100 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 rounded-xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="space-y-1 text-center sm:text-left rtl:sm:text-right w-full overflow-hidden">
            <div className="text-[10px] font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400">
              TON / USDT (TON Network Wallet Address)
            </div>
            <div className="font-mono text-xs text-slate-800 dark:text-slate-200 font-bold break-all">
              {WALLET_ADDRESS}
            </div>
          </div>

          <button
            onClick={handleCopyWallet}
            className={`flex items-center space-x-1.5 rtl:space-x-reverse px-4 py-2.5 rounded-xl font-bold text-xs transition-all shrink-0 shadow-sm ${
              copied
                ? "bg-emerald-600 text-white"
                : "bg-amber-600 hover:bg-amber-700 text-white"
            }`}
          >
            {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? t.walletCopied : t.copyWallet}</span>
          </button>
        </div>
      </div>

      {/* Release Management & GitHub Releases */}
      <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center space-x-3 rtl:space-x-reverse text-indigo-600 dark:text-indigo-400">
          <div className="p-2.5 bg-indigo-500/10 rounded-xl">
            <Tag className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">{t.releaseGuide} & GitHub Releases</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">How releases are published and updated for user downloads</p>
          </div>
        </div>

        {/* Latest Release info if available */}
        {latestRelease ? (
          <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-700 dark:text-emerald-400 flex items-center space-x-1.5 rtl:space-x-reverse">
                <Sparkles className="w-4 h-4" />
                <span>Latest GitHub Release: {latestRelease.tag_name}</span>
              </span>
              <a
                href={latestRelease.html_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline inline-flex items-center space-x-1"
              >
                <span>View Release</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-2">{latestRelease.body || "No changelog notes provided."}</p>
          </div>
        ) : (
          <div className="text-xs text-slate-500 italic">
            {loadingRelease ? "Checking GitHub Releases..." : "No GitHub release fetched yet."}
          </div>
        )}

        <div className="space-y-3 pt-2 text-xs text-slate-600 dark:text-slate-300">
          <h3 className="font-bold text-slate-900 dark:text-white flex items-center space-x-2 rtl:space-x-reverse">
            <HelpCircle className="w-4 h-4 text-indigo-500" />
            <span>How to publish a new release on GitHub:</span>
          </h3>

          <ol className="list-decimal list-inside space-y-2 leading-relaxed bg-slate-50 dark:bg-slate-900/60 p-4 rounded-xl border border-slate-200 dark:border-slate-700/60 font-mono text-[11px]">
            <li>1. Update version number in <span className="text-indigo-600 dark:text-indigo-400 font-bold">VERSION</span> and <span className="text-indigo-600 dark:text-indigo-400 font-bold">app/config/constants.py</span></li>
            <li>2. Build Windows executable: <span className="text-amber-600 dark:text-amber-400">.\build.ps1</span> (creates OptiPixel-Installer.exe)</li>
            <li>3. Create and push tag: <span className="text-emerald-600 dark:text-emerald-400">git tag -a v0.2.0 -m "Release v0.2.0" && git push origin v0.2.0</span></li>
            <li>4. Go to <a href={`${REPO_URL}/releases/new`} target="_blank" rel="noopener noreferrer" className="text-indigo-500 underline">github.com/{GITHUB_USER}/{REPO_NAME}/releases/new</a></li>
            <li>5. Attach installer executable and publish!</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

