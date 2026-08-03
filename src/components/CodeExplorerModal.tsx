import React, { useEffect, useState } from "react";
import { Code, Copy, Check, Download, FileCode, FolderTree } from "lucide-react";

export const CodeExplorerModal: React.FC = () => {
  const [fileMap, setFileMap] = useState<Record<string, string>>({});
  const [selectedFile, setSelectedFile] = useState<string>("app/main.py");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetch("/api/python-code")
      .then((res) => res.json())
      .then((data) => {
        if (data.files) {
          setFileMap(data.files);
        }
      })
      .catch((err) => console.error("Error fetching code:", err));
  }, []);

  const copyToClipboard = () => {
    const code = fileMap[selectedFile] || "";
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const fileList = Object.keys(fileMap);

  return (
    <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-700/60 pb-3">
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-900/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
            <Code className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Python PySide6 Desktop Repository Explorer</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Complete source code, PyInstaller build scripts, and Inno Setup installer</p>
          </div>
        </div>

        <button
          onClick={copyToClipboard}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs px-3.5 py-2 rounded-xl transition-all shadow-md flex items-center space-x-1.5"
        >
          {copied ? <Check className="w-4 h-4 text-emerald-300" /> : <Copy className="w-4 h-4" />}
          <span>{copied ? "Copied!" : "Copy Selected File"}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-[550px]">
        {/* File Tree List (4 Cols) */}
        <div className="md:col-span-4 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl p-2 overflow-y-auto space-y-1">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2 py-1 flex items-center space-x-1">
            <FolderTree className="w-3.5 h-3.5" />
            <span>Repository Files</span>
          </div>

          {fileList.map((fileName) => {
            const isSelected = selectedFile === fileName;
            return (
              <button
                key={fileName}
                onClick={() => setSelectedFile(fileName)}
                className={`w-full text-left rtl:text-right px-2.5 py-1.5 rounded-lg text-xs font-mono truncate transition-all flex items-center space-x-2 ${
                  isSelected
                    ? "bg-indigo-600 text-white font-bold shadow-sm"
                    : "text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800"
                }`}
              >
                <FileCode className="w-3.5 h-3.5 shrink-0 opacity-70" />
                <span className="truncate">{fileName}</span>
              </button>
            );
          })}
        </div>

        {/* Code Editor Preview (8 Cols) */}
        <div className="md:col-span-8 bg-slate-950 text-slate-200 border border-slate-800 rounded-xl p-4 overflow-auto font-mono text-xs leading-relaxed">
          <div className="text-slate-500 font-bold border-b border-slate-800 pb-2 mb-3 flex justify-between items-center">
            <span>{selectedFile}</span>
            <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
              {(fileMap[selectedFile] || "").split("\n").length} lines
            </span>
          </div>
          <pre>{fileMap[selectedFile] || "# File empty or loading..."}</pre>
        </div>
      </div>
    </div>
  );
};
