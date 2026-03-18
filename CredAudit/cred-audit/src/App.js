import { useState } from "react";

const nodes = {
  main: {
    id: "main", label: "main.py", lang: "Python", color: "#3b82f6",
    description: "Orchestrator. Handles --audit, --config, and --report args via argparse. Calls C# for config validation and report generation, runs the audit pipeline.",
    position: { x: 340, y: 20 },
  },
  config: {
    id: "config", label: "config.json", lang: "Config", color: "#8b5cf6",
    description: "Stores settings: hash_type (auto/md5/sha1/sha256), wordlist_path, check_breaches toggle, and output_folder. Edited via the rich terminal UI.",
    position: { x: 80, y: 160 },
  },
  recon1: {
    id: "recon1", label: "ReconProcessor\n--config mode", lang: "C#", color: "#10b981",
    description: "Validates config.json before any auditing starts. Checks hash_type is valid, wordlist path exists, and output folder is set. Exits with code 1 if invalid.",
    position: { x: 330, y: 160 },
  },
  hashid: {
    id: "hashid", label: "hash_identifier.py", lang: "Python", color: "#3b82f6",
    description: "Detects hash type from a given hash string using length and character patterns. Returns MD5, SHA1, SHA256, bcrypt etc. Used before cracking so you don't need to specify the type manually.",
    position: { x: 40, y: 320 },
  },
  cracker: {
    id: "cracker", label: "wordlist_cracker.py", lang: "Python", color: "#3b82f6",
    description: "Takes a hash and a wordlist file. Hashes each word with hashlib and compares to the target. Returns the plaintext password if found. Supports MD5, SHA1, SHA256.",
    position: { x: 220, y: 320 },
  },
  scorer: {
    id: "scorer", label: "strength_scorer.py", lang: "Python", color: "#3b82f6",
    description: "Scores a plaintext password 0-100. Checks length, uppercase, lowercase, numbers, symbols, and common patterns like 'password123'. Returns a grade: WEAK / FAIR / STRONG / VERY STRONG.",
    position: { x: 400, y: 320 },
  },
  hibp: {
    id: "hibp", label: "hibp_checker.py", lang: "Python", color: "#3b82f6",
    description: "Uses HaveIBeenPwned's k-anonymity API. Sends only the first 5 chars of the SHA1 hash — never the full password. Returns how many times the password appeared in real breach data.",
    position: { x: 590, y: 320 },
  },
  results: {
    id: "results", label: "results.json", lang: "Data", color: "#8b5cf6",
    description: "Central data file. Stores the hash, detected type, cracked plaintext, strength score/grade/feedback, and breach count. Written by Python, read by C# for the report.",
    position: { x: 340, y: 480 },
  },
  history: {
    id: "history", label: "history.json", lang: "Data", color: "#8b5cf6",
    description: "Cumulative list of all past audit results. Every run appends the latest results.json entry. Lets you track audits over time.",
    position: { x: 100, y: 480 },
  },
  recon2: {
    id: "recon2", label: "ReconProcessor\n--report mode", lang: "C#", color: "#10b981",
    description: "Reads results.json and builds a color-coded HTML report. Shows hash type, cracked value, strength grade, and breach count. Uses StringBuilder just like ReconKit.",
    position: { x: 340, y: 620 },
  },
  report: {
    id: "report", label: "report.html", lang: "Output", color: "#ef4444",
    description: "Final output. Color-coded HTML showing the full audit — cracked passwords highlighted in red, strong passwords in green, breach counts, and strength feedback.",
    position: { x: 340, y: 760 },
  },
};

const edges = [
  { from: "main", to: "config", label: "reads" },
  { from: "main", to: "recon1", label: "calls" },
  { from: "config", to: "recon1", label: "validates" },
  { from: "recon1", to: "hashid", label: "triggers" },
  { from: "recon1", to: "cracker", label: "triggers" },
  { from: "recon1", to: "scorer", label: "triggers" },
  { from: "recon1", to: "hibp", label: "triggers" },
  { from: "hashid", to: "cracker", label: "type →" },
  { from: "cracker", to: "results", label: "writes" },
  { from: "scorer", to: "results", label: "writes" },
  { from: "hibp", to: "results", label: "writes" },
  { from: "results", to: "history", label: "appended to" },
  { from: "results", to: "recon2", label: "read by" },
  { from: "recon2", to: "report", label: "generates" },
];

const langColors = {
  Python: "#3b82f6", "C#": "#10b981", Config: "#8b5cf6",
  Data: "#8b5cf6", Output: "#ef4444",
};

const weeks = [
  {
    week: 1, title: "Hash ID + Wordlist Cracker", color: "#3b82f6",
    tasks: [
      { text: "Set up project structure and config.json", file: null },
      { text: "Write hash_identifier.py using length + pattern detection", file: "hash_identifier.py" },
      { text: "Generate test hashes with Python's hashlib", file: null },
      { text: "Write wordlist_cracker.py to crack MD5/SHA1/SHA256", file: "wordlist_cracker.py" },
      { text: "Download a wordlist (rockyou.txt or similar)", file: null },
      { text: "Write cracked results to results.json", file: "results.json" },
    ],
    learn: "How hashing works, rainbow tables, wordlist attacks",
  },
  {
    week: 2, title: "Strength Scorer + HIBP", color: "#8b5cf6",
    tasks: [
      { text: "Write strength_scorer.py with length/complexity checks", file: "strength_scorer.py" },
      { text: "Add common pattern detection (password123, qwerty, etc.)", file: "strength_scorer.py" },
      { text: "pip install requests for API calls", file: null },
      { text: "Write hibp_checker.py using k-anonymity API", file: "hibp_checker.py" },
      { text: "Understand why only 5 chars of the hash are sent", file: null },
      { text: "Append strength + breach data to results.json", file: "results.json" },
    ],
    learn: "Password strength rules, k-anonymity, breach databases",
  },
  {
    week: 3, title: "C# Config + Report Generator", color: "#10b981",
    tasks: [
      { text: "Create ReportGenerator C# console app", file: null },
      { text: "Write Models.cs to match results.json structure", file: "Models.cs" },
      { text: "Write ConfigLoader.cs to validate config.json", file: "ConfigLoader.cs" },
      { text: "Write ReportGenerator.cs using StringBuilder", file: "ReportGenerator.cs" },
      { text: "Color-code output: red for weak/breached, green for strong", file: "ReportGenerator.cs" },
      { text: "Wire --config and --report into Program.cs", file: "Program.cs" },
    ],
    learn: "C# JSON deserialization, HTML generation, subprocess calls",
  },
  {
    week: 4, title: "main.py + UI + Polish", color: "#ef4444",
    tasks: [
      { text: "Write main.py with --audit, --config, --report args", file: "main.py" },
      { text: "Wire C# config validation before every audit", file: "main.py" },
      { text: "Write rich terminal UI for inputting hashes", file: "ui.py" },
      { text: "Add history.json append logic to FileHandler", file: "file_handler.py" },
      { text: "Write a solid README explaining the project", file: null },
      { text: "Commit everything to GitHub!", file: null },
    ],
    learn: "Full pipeline automation, CLI design, project documentation",
  },
];

function getCenter(node) {
  const w = 160, h = 48;
  return { x: node.position.x + w / 2, y: node.position.y + h / 2 };
}

export default function App() {
  const [tab, setTab] = useState("flow");
  const [selected, setSelected] = useState(null);
  const [checked, setChecked] = useState({});
  const active = selected ? nodes[selected] : null;

  const toggleCheck = (key) => setChecked(p => ({ ...p, [key]: !p[key] }));
  const totalTasks = weeks.reduce((a, w) => a + w.tasks.length, 0);
  const doneTasks = Object.values(checked).filter(Boolean).length;
  const progress = Math.round((doneTasks / totalTasks) * 100);

  return (
    <div style={{ fontFamily: "sans-serif", background: "#0f172a", minHeight: "100vh", color: "#f1f5f9" }}>
      <div style={{ padding: "24px 24px 0" }}>
        <h2 style={{ textAlign: "center", marginBottom: 4, fontSize: 22, fontWeight: 700, letterSpacing: 1 }}>CredAudit</h2>
        <p style={{ textAlign: "center", color: "#94a3b8", marginBottom: 20, fontSize: 13 }}>Password Auditor & Credential Analyzer</p>
        <div style={{ display: "flex", justifyContent: "center", gap: 8, marginBottom: 24 }}>
          {["flow", "roadmap"].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "8px 28px", borderRadius: 8, border: "none", cursor: "pointer",
              fontSize: 14, fontWeight: 600, transition: "all 0.15s",
              background: tab === t ? "#3b82f6" : "#1e293b",
              color: tab === t ? "#fff" : "#94a3b8",
            }}>{t === "flow" ? "🔐 File Flow" : "🗺️ Roadmap"}</button>
          ))}
        </div>
      </div>

      {tab === "flow" && (
        <div style={{ padding: "0 24px 24px" }}>
          <div style={{ display: "flex", gap: 16, justifyContent: "center", marginBottom: 16, flexWrap: "wrap" }}>
            {Object.entries(langColors).map(([lang, color]) => (
              <div key={lang} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12 }}>
                <div style={{ width: 12, height: 12, borderRadius: 3, background: color }} />
                <span style={{ color: "#cbd5e1" }}>{lang}</span>
              </div>
            ))}
          </div>
          <div style={{
            minHeight: 80, background: "#1e293b",
            border: `1.5px solid ${active ? langColors[active.lang] : "#334155"}`,
            borderRadius: 10, padding: "14px 20px",
            maxWidth: 780, margin: "0 auto 20px auto", transition: "border-color 0.2s",
          }}>
            {active ? (
              <>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                  <span style={{ background: langColors[active.lang], color: "#fff", borderRadius: 5, padding: "2px 10px", fontSize: 11, fontWeight: 700 }}>{active.lang}</span>
                  <span style={{ fontWeight: 700, fontSize: 15 }}>{active.label.replace("\n", " ")}</span>
                </div>
                <p style={{ color: "#cbd5e1", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{active.description}</p>
              </>
            ) : (
              <p style={{ color: "#475569", margin: 0, fontSize: 13, textAlign: "center", paddingTop: 22 }}>Click any node below to see what it does</p>
            )}
          </div>
          <div style={{ overflowX: "auto" }}>
            <svg width={780} height={840} style={{ display: "block", margin: "0 auto" }}>
              <defs>
                <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
                  <path d="M0,0 L0,6 L8,3 z" fill="#475569" />
                </marker>
              </defs>
              {edges.map((e, i) => {
                const f = getCenter(nodes[e.from]), t = getCenter(nodes[e.to]);
                const mx = (f.x + t.x) / 2, my = (f.y + t.y) / 2;
                const dx = t.x - f.x, dy = t.y - f.y;
                const len = Math.sqrt(dx * dx + dy * dy) || 1;
                const nx = (-dy / len) * 18, ny = (dx / len) * 18;
                return (
                  <g key={i}>
                    <line x1={f.x} y1={f.y} x2={t.x} y2={t.y} stroke="#334155" strokeWidth={1.5} markerEnd="url(#arrow)" />
                    <text x={mx + nx} y={my + ny} fontSize={10} fill="#64748b" textAnchor="middle" dominantBaseline="middle" style={{ userSelect: "none" }}>{e.label}</text>
                  </g>
                );
              })}
              {Object.values(nodes).map((node) => {
                const w = 160, h = 48, isSelected = selected === node.id;
                const lines = node.label.split("\n");
                return (
                  <g key={node.id} transform={`translate(${node.position.x},${node.position.y})`} style={{ cursor: "pointer" }} onClick={() => setSelected(isSelected ? null : node.id)}>
                    <rect width={w} height={h} rx={8}
                      fill={isSelected ? node.color : "#1e293b"}
                      stroke={node.color} strokeWidth={isSelected ? 2.5 : 1.5}
                      style={{ transition: "all 0.15s" }}
                    />
                    {lines.map((line, li) => (
                      <text key={li} x={w / 2} y={lines.length === 1 ? h / 2 : (li === 0 ? 16 : 34)}
                        textAnchor="middle" dominantBaseline="middle"
                        fontSize={11} fontWeight={600}
                        fill={isSelected ? "#fff" : "#e2e8f0"}
                        style={{ pointerEvents: "none", userSelect: "none" }}
                      >{line}</text>
                    ))}
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      )}

      {tab === "roadmap" && (
        <div style={{ padding: "0 24px 40px", maxWidth: 800, margin: "0 auto" }}>
          <div style={{ background: "#1e293b", borderRadius: 10, padding: "16px 20px", marginBottom: 28 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <span style={{ fontSize: 13, color: "#94a3b8" }}>Overall Progress</span>
              <span style={{ fontSize: 13, fontWeight: 700 }}>{doneTasks}/{totalTasks} tasks</span>
            </div>
            <div style={{ background: "#0f172a", borderRadius: 999, height: 10, overflow: "hidden" }}>
              <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg, #3b82f6, #10b981)", borderRadius: 999, transition: "width 0.3s" }} />
            </div>
            <div style={{ textAlign: "right", fontSize: 12, color: "#64748b", marginTop: 4 }}>{progress}% complete</div>
          </div>
          {weeks.map((w) => {
            const weekDone = w.tasks.filter((_, i) => checked[`${w.week}-${i}`]).length;
            return (
              <div key={w.week} style={{ background: "#1e293b", borderRadius: 12, marginBottom: 20, overflow: "hidden" }}>
                <div style={{ background: w.color + "22", borderLeft: `4px solid ${w.color}`, padding: "14px 20px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <span style={{ fontSize: 11, fontWeight: 700, color: w.color, letterSpacing: 1, textTransform: "uppercase" }}>Week {w.week}</span>
                    <h3 style={{ margin: "2px 0 0", fontSize: 16, fontWeight: 700 }}>{w.title}</h3>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 12, color: "#64748b" }}>{weekDone}/{w.tasks.length}</div>
                    <div style={{ background: "#0f172a", borderRadius: 999, height: 6, width: 80, marginTop: 4, overflow: "hidden" }}>
                      <div style={{ width: `${(weekDone / w.tasks.length) * 100}%`, height: "100%", background: w.color, borderRadius: 999, transition: "width 0.3s" }} />
                    </div>
                  </div>
                </div>
                <div style={{ padding: "12px 20px" }}>
                  {w.tasks.map((task, i) => {
                    const key = `${w.week}-${i}`;
                    const done = checked[key];
                    return (
                      <div key={i} onClick={() => toggleCheck(key)}
                        style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 4px", cursor: "pointer", borderRadius: 6 }}
                        onMouseEnter={e => e.currentTarget.style.background = "#0f172a"}
                        onMouseLeave={e => e.currentTarget.style.background = "transparent"}
                      >
                        <div style={{
                          width: 18, height: 18, borderRadius: 4, flexShrink: 0,
                          border: `2px solid ${done ? w.color : "#475569"}`,
                          background: done ? w.color : "transparent",
                          display: "flex", alignItems: "center", justifyContent: "center", transition: "all 0.15s",
                        }}>
                          {done && <span style={{ color: "#fff", fontSize: 11, fontWeight: 700 }}>✓</span>}
                        </div>
                        <span style={{ fontSize: 13, flex: 1, color: done ? "#475569" : "#cbd5e1", textDecoration: done ? "line-through" : "none" }}>{task.text}</span>
                        {task.file && (
                          <span style={{ fontSize: 11, color: "#64748b", background: "#0f172a", padding: "2px 8px", borderRadius: 4, fontFamily: "monospace", flexShrink: 0 }}>{task.file}</span>
                        )}
                      </div>
                    );
                  })}
                </div>
                <div style={{ padding: "4px 20px 14px" }}>
                  <span style={{ fontSize: 11, color: "#64748b" }}>📚 You'll learn: </span>
                  <span style={{ fontSize: 11, color: "#94a3b8" }}>{w.learn}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}